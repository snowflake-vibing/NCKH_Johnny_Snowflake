"""Multi-source TAWOS dataset builder, cleaner, and HF uploader (no MySQL required for TAWOS.sql).

Supported sources (`--source`):
- `auto`: automatically detects TAWOS.sql(.gz/.zip), interim parquets, existing snapshots, or MySQL env.
- `sql`: 2-pass streaming pure-Python parser for `TAWOS.sql` (handles Change_Log -> Issue -> Project dump order).
- `interim`: loads `<PROJECT>_issue.parquet` and `<PROJECT>_changelog.parquet` and builds planning-time snapshots.
- `snapshot`: validates, normalizes, audits, and packages existing `<PROJECT>_snapshot.{parquet,csv}` files.
- `mysql`: extracts directly from local/remote MySQL `tawos` database via SQLAlchemy + PyMySQL.

Reconstructs planning-time state using exact parity with JohnnyPhan1712/SR-G3_planning-time-sp (`src/snapshot.py`)
and uploads `<PROJECT>_snapshot.parquet` + `dataset_summary.csv` + `metadata.json` to Hugging Face in 1 commit.
"""

from __future__ import annotations

import argparse
import glob
import gzip
import io
import os
import re
import sys
import time
import urllib.request
import zipfile
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Set, Tuple

import numpy as np
import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    from kaggle_TAWOS.config import (
        DEFAULT_RESULTS_REPO_NAME,
        DEFAULT_SNAPSHOTS_SUBDIR,
        MAX_SP,
        SNAPSHOT_REQUIRED_COLS,
        SP_FIELDS,
        SPLIT,
        TEXT_FIELDS,
        parse_projects_arg,
        resolve_data_dir,
    )
    from kaggle_TAWOS.hf_utils import HFExperimentLogger
except ImportError:
    from config import (  # type: ignore
        DEFAULT_RESULTS_REPO_NAME,
        DEFAULT_SNAPSHOTS_SUBDIR,
        MAX_SP,
        SNAPSHOT_REQUIRED_COLS,
        SP_FIELDS,
        SPLIT,
        TEXT_FIELDS,
        parse_projects_arg,
        resolve_data_dir,
    )
    from hf_utils import HFExperimentLogger  # type: ignore


TARGET_CHANGELOG_FIELDS = set(SP_FIELDS) | set(TEXT_FIELDS.keys())

DEFAULT_TABLE_COLS: Dict[str, List[str]] = {
    "Project": [
        "ID", "Project_Key", "Name", "URL", "Description",
        "Start_Date", "Last_Update_Date", "SP_Field_ID", "Repository_ID",
    ],
    "Issue": [
        "ID", "Jira_ID", "Issue_Key", "URL", "Title", "Description",
        "Description_Text", "Description_Code", "Type", "Priority", "Status",
        "Resolution", "Creation_Date", "Estimation_Date", "Resolution_Date",
        "Last_Updated", "Story_Point", "Timespent", "In_Progress_Minutes",
        "Total_Effort_Minutes", "Resolution_Time_Minutes",
        "Title_Changed_After_Estimation", "Description_Changed_After_Estimation",
        "Story_Point_Changed_After_Estimation", "Pull_Request_URL",
        "Creator_ID", "Reporter_ID", "Assignee_ID", "Project_ID", "Sprint_ID",
    ],
    "Change_Log": [
        "ID", "Issue_ID", "Author_ID", "Field", "From_Value", "To_Value",
        "From_String", "To_String", "Change_Type", "Creation_Date",
    ],
}

MYSQL_SQL = {
    "issue": (
        "SELECT i.* FROM Issue i "
        "JOIN Project p ON p.ID = i.Project_ID "
        "WHERE p.Project_Key = :key"
    ),
    "changelog": (
        "SELECT c.* FROM Change_Log c "
        "JOIN Issue i ON i.ID = c.Issue_ID "
        "JOIN Project p ON p.ID = i.Project_ID "
        "WHERE p.Project_Key = :key"
    ),
}

_MYSQL_ESCAPES = {
    "0": "\0",
    "b": "\b",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "Z": "\x1a",
    "'": "'",
    '"': '"',
    "\\": "\\",
}


# ---------------------------------------------------------------------------
# Core Planning-Time Snapshot Reconstruction (parity with src/snapshot.py)
# ---------------------------------------------------------------------------

def _clean(s: pd.Series, quoted: bool = False) -> pd.Series:
    """Normalize CSV-quoted Issue text and Change_Log text into one consistent whitespace format."""
    s = s.astype("string")
    if quoted:
        q = s.str.startswith('"', na=False) & s.str.endswith('"', na=False) & (s.str.len() >= 2)
        s = s.where(~q, s.str[1:-1].str.replace('""', '"'))
    return s.str.split().str.join(" ")


def _value_at(final: pd.Series, log: pd.DataFrame, t: pd.Series) -> pd.Series:
    """Restore per-issue field value at time t using From_String of first post-planning change."""
    if log is None or len(log) == 0:
        return final.astype(object)
    after = log[log.Creation_Date > log.Issue_ID.map(t)].drop_duplicates("Issue_ID").set_index("Issue_ID")
    v = final.astype(object)
    v.loc[after.index] = _clean(after.From_String)
    return v


def build_snapshot(issue: pd.DataFrame, changelog: pd.DataFrame) -> pd.DataFrame:
    """Build planning-time snapshot DataFrame from Issue and Change_Log tables."""
    iss = issue[issue.Story_Point.notna()].copy()
    if iss.empty:
        return pd.DataFrame(columns=SNAPSHOT_REQUIRED_COLS)

    iss["ID"] = pd.to_numeric(iss["ID"], errors="raise").astype("int64")
    iss["Creation_Date"] = pd.to_datetime(iss["Creation_Date"], errors="coerce")
    iss["Story_Point"] = pd.to_numeric(iss["Story_Point"], errors="coerce")
    iss = iss.set_index("ID")

    if changelog is None or len(changelog) == 0:
        log = pd.DataFrame(
            columns=["ID", "Issue_ID", "Field", "From_String", "To_String", "Creation_Date"]
        )
    else:
        log = changelog[changelog.Issue_ID.isin(iss.index)].copy()
        log["ID"] = pd.to_numeric(log["ID"], errors="coerce")
        log["Issue_ID"] = pd.to_numeric(log["Issue_ID"], errors="coerce")
        log["Creation_Date"] = pd.to_datetime(log["Creation_Date"], errors="coerce")
        log = log.sort_values(["Creation_Date", "ID"])

    field = log.Field.astype("string").str.lower()

    first = log[field.isin(SP_FIELDS)].drop_duplicates("Issue_ID").set_index("Issue_ID")
    later = first.index[first.From_String.isna()]
    at_creation = first.index.difference(later)

    t = iss.Creation_Date.copy()
    if len(later) > 0:
        t.loc[later] = first.Creation_Date[later]

    sp = iss.Story_Point.astype(object)
    if len(later) > 0:
        sp.loc[later] = first.To_String[later]
    if len(at_creation) > 0:
        sp.loc[at_creation] = first.From_String[at_creation]

    out = pd.DataFrame(
        {
            "Issue_Key": iss.Issue_Key.astype(str),
            "Creation_Date": iss.Creation_Date,
            "Planning_Date": pd.to_datetime(t, errors="coerce"),
            "Story_Point": pd.to_numeric(sp, errors="coerce").astype("float64"),
            "Final_Story_Point": pd.to_numeric(iss.Story_Point, errors="coerce").astype("float64"),
        }
    )
    for f, col in TEXT_FIELDS.items():
        final = _clean(iss[col], quoted=True)
        out[col] = _value_at(final, log[field == f], t).astype("string")
        out["Final_" + col] = final.astype("string")
    return out.reset_index(names="ID")


def normalize_existing_snapshot(df: pd.DataFrame, project: str) -> pd.DataFrame:
    """Validate and standardize an existing snapshot DataFrame without double-unquoting text."""
    missing = [c for c in SNAPSHOT_REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"[{project}] Existing snapshot missing required columns: {missing}")

    out = df[SNAPSHOT_REQUIRED_COLS].copy()
    out["ID"] = pd.to_numeric(out["ID"], errors="raise").astype("int64")
    out["Issue_Key"] = out["Issue_Key"].astype(str)
    out["Creation_Date"] = pd.to_datetime(out["Creation_Date"], errors="coerce")
    out["Planning_Date"] = pd.to_datetime(out["Planning_Date"], errors="coerce")
    out["Story_Point"] = pd.to_numeric(out["Story_Point"], errors="coerce").astype("float64")
    out["Final_Story_Point"] = pd.to_numeric(out["Final_Story_Point"], errors="coerce").astype("float64")
    for col in ("Title", "Final_Title", "Description", "Final_Description"):
        out[col] = _clean(out[col], quoted=False)
    return out


# ---------------------------------------------------------------------------
# Pure-Python 2-Pass Streaming MySQL Dump Parser (`TAWOS.sql`)
# ---------------------------------------------------------------------------

@contextmanager
def open_sql_text_stream(sql_path: str) -> Iterator[io.TextIOBase]:
    """Open plain `.sql`, `.sql.gz`, or `.sql.zip` seamlessly as a UTF-8 text stream."""
    lower = sql_path.lower()
    if lower.endswith(".gz"):
        with gzip.open(sql_path, "rt", encoding="utf-8", errors="replace") as fh:
            yield fh
    elif lower.endswith(".zip"):
        with zipfile.ZipFile(sql_path, "r") as zf:
            sql_members = [m for m in zf.namelist() if m.lower().endswith(".sql") and not m.startswith("__MACOSX/")]
            if not sql_members:
                raise FileNotFoundError(f"No .sql entry found inside zip archive: {sql_path}")
            member = sql_members[0]
            with zf.open(member, "r") as raw_bin:
                with io.TextIOWrapper(raw_bin, encoding="utf-8", errors="replace") as txt:
                    yield txt
    else:
        with open(sql_path, "rt", encoding="utf-8", errors="replace") as fh:
            yield fh


def _extract_insert_table_and_header(stmt: str) -> Tuple[Optional[str], Optional[List[str]], int]:
    """Parse table name, optional column list, and char index immediately after VALUES."""
    m = re.match(r"^\s*INSERT\s+(?:IGNORE\s+)?INTO\s+`?([A-Za-z0-9_]+)`?\s*", stmt, flags=re.IGNORECASE)
    if not m:
        return None, None, -1
    table_name = m.group(1)
    pos = m.end()
    n = len(stmt)
    while pos < n and stmt[pos].isspace():
        pos += 1

    cols: Optional[List[str]] = None
    if pos < n and stmt[pos] == "(":
        end_col = stmt.find(")", pos + 1)
        if end_col != -1:
            raw_cols = stmt[pos + 1 : end_col]
            cols = [c.strip().strip("`").strip('"') for c in raw_cols.split(",") if c.strip()]
            pos = end_col + 1

    m_val = re.search(r"\bVALUES\b", stmt[pos:], flags=re.IGNORECASE)
    if not m_val:
        return table_name, cols, -1
    val_start = pos + m_val.end()
    return table_name, cols, val_start


def iter_insert_rows(stmt: str, val_start: int) -> Iterator[List[Optional[str]]]:
    """Yield decoded field lists from a MySQL `INSERT INTO ... VALUES (...),(...);` statement."""
    n = len(stmt)
    i = val_start

    while i < n:
        while i < n and stmt[i] in " \t\r\n,":
            i += 1
        if i >= n or stmt[i] == ";":
            break
        if stmt[i] != "(":
            i += 1
            continue

        i += 1  # consume '('
        row: List[Optional[str]] = []
        while i < n:
            while i < n and stmt[i] in " \t\r\n":
                i += 1
            if i >= n:
                break
            if stmt[i] == ")":
                i += 1
                break

            # Handle optional charset/binary introducer like `_binary '...'`
            if stmt[i] == "_":
                j = i + 1
                while j < n and (stmt[j].isalnum() or stmt[j] == "_"):
                    j += 1
                while j < n and stmt[j] in " \t":
                    j += 1
                if j < n and stmt[j] == "'":
                    i = j

            if stmt[i] == "'":
                i += 1
                chars: List[str] = []
                while i < n:
                    ch = stmt[i]
                    if ch == "\\" and i + 1 < n:
                        nxt = stmt[i + 1]
                        chars.append(_MYSQL_ESCAPES.get(nxt, nxt))
                        i += 2
                    elif ch == "'":
                        if i + 1 < n and stmt[i + 1] == "'":
                            chars.append("'")
                            i += 2
                        else:
                            i += 1
                            break
                    else:
                        chars.append(ch)
                        i += 1
                row.append("".join(chars))
                while i < n and stmt[i] in " \t\r\n":
                    i += 1
                if i < n and stmt[i] == ",":
                    i += 1
                elif i < n and stmt[i] == ")":
                    i += 1
                    break
            else:
                start = i
                while i < n and stmt[i] not in ",)":
                    i += 1
                tok = stmt[start:i].strip()
                if tok.upper() == "NULL":
                    row.append(None)
                else:
                    row.append(tok)
                if i < n and stmt[i] == ",":
                    i += 1
                elif i < n and stmt[i] == ")":
                    i += 1
                    break

        yield row


def _statement_ends_outside_quotes(chunk: str, in_quote: bool, escape: bool) -> Tuple[bool, bool, bool]:
    """Track single-quote & escape state across lines to know when a SQL INSERT finishes."""
    for ch in chunk:
        if escape:
            escape = False
            continue
        if ch == "\\":
            if in_quote:
                escape = True
            continue
        if ch == "'":
            in_quote = not in_quote
    stripped = chunk.rstrip()
    done = (not in_quote) and (not escape) and stripped.endswith(";")
    return done, in_quote, escape


def _iter_table_inserts(
    sql_path: str, target_tables: Set[str]
) -> Tuple[Dict[str, List[str]], Iterator[Tuple[str, Optional[List[str]], List[Optional[str]]]]]:
    """First scan CREATE TABLE definitions, then yield rows for `target_tables`."""
    # Because callers iterate lazily, return a single-pass generator + shared schema dict.
    table_cols: Dict[str, List[str]] = {k: list(v) for k, v in DEFAULT_TABLE_COLS.items()}
    canonical_targets = {t.lower(): t for t in target_tables}

    def _row_generator() -> Iterator[Tuple[str, Optional[List[str]], List[Optional[str]]]]:
        in_create_table: Optional[str] = None
        parsed_cols: List[str] = []

        collecting_insert_table: Optional[str] = None
        buf_lines: List[str] = []
        in_quote = False
        escape = False

        with open_sql_text_stream(sql_path) as fh:
            for line in fh:
                if collecting_insert_table is not None:
                    buf_lines.append(line)
                    done, in_quote, escape = _statement_ends_outside_quotes(line, in_quote, escape)
                    if done:
                        stmt = "".join(buf_lines)
                        buf_lines.clear()
                        tbl_name, explicit_cols, val_start = _extract_insert_table_and_header(stmt)
                        canon_tbl = canonical_targets.get((tbl_name or collecting_insert_table).lower(), collecting_insert_table)
                        collecting_insert_table = None
                        if val_start != -1:
                            for row in iter_insert_rows(stmt, val_start):
                                yield canon_tbl, explicit_cols, row
                    continue

                if in_create_table is not None:
                    s_line = line.lstrip()
                    if s_line.startswith(")"):
                        if parsed_cols:
                            table_cols[in_create_table] = parsed_cols
                        in_create_table = None
                        parsed_cols = []
                    elif s_line.startswith("`"):
                        col_end = s_line.find("`", 1)
                        if col_end > 1:
                            parsed_cols.append(s_line[1:col_end])
                    continue

                s_line = line.lstrip()
                if s_line[:12].upper() == "CREATE TABLE":
                    m_ct = re.match(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?([A-Za-z0-9_]+)`?", s_line, re.I)
                    if m_ct:
                        t_raw = m_ct.group(1)
                        for std_name in DEFAULT_TABLE_COLS:
                            if std_name.lower() == t_raw.lower():
                                if not s_line.rstrip().endswith(";"):
                                    in_create_table = std_name
                                    parsed_cols = []
                                break
                    continue

                if s_line[:6].upper() == "INSERT":
                    m_ins = re.match(r"INSERT\s+(?:IGNORE\s+)?INTO\s+`?([A-Za-z0-9_]+)`?", s_line, re.I)
                    if m_ins:
                        t_key = m_ins.group(1).lower()
                        if t_key in canonical_targets:
                            canon_tbl = canonical_targets[t_key]
                            done, in_quote, escape = _statement_ends_outside_quotes(line, False, False)
                            if done:
                                _, explicit_cols, val_start = _extract_insert_table_and_header(line)
                                if val_start != -1:
                                    for row in iter_insert_rows(line, val_start):
                                        yield canon_tbl, explicit_cols, row
                            else:
                                collecting_insert_table = canon_tbl
                                buf_lines = [line]

    return table_cols, _row_generator()


def build_snapshots_from_sql(
    sql_path: str, projects: Sequence[str]
) -> Dict[str, pd.DataFrame]:
    """2-pass streaming parser building per-project snapshot DataFrames straight from TAWOS.sql."""
    target_set = {p.upper() for p in projects}
    print(f"🔎 [SQL Pass 1/2] Scanning Project & Issue tables in {sql_path} ...")

    proj_key_by_id: Dict[int, str] = {}
    issues_by_pid: Dict[int, List[Tuple[int, str, str, float, Optional[str], Optional[str]]]] = {}

    table_cols, gen1 = _iter_table_inserts(sql_path, {"Project", "Issue"})
    for tbl, explicit_cols, row in gen1:
        cols = explicit_cols or table_cols[tbl]
        idx = {c: pos for pos, c in enumerate(cols)}
        if tbl == "Project":
            if len(row) <= max(idx["ID"], idx["Project_Key"]):
                continue
            pid_raw = row[idx["ID"]]
            pkey_raw = row[idx["Project_Key"]]
            if pid_raw is None or pkey_raw is None:
                continue
            pkey = str(pkey_raw).strip().upper()
            if pkey in target_set:
                proj_key_by_id[int(pid_raw)] = pkey
        elif tbl == "Issue":
            needed = (idx["ID"], idx["Issue_Key"], idx["Creation_Date"], idx["Story_Point"], idx["Title"], idx["Description"], idx["Project_ID"])
            if len(row) <= max(needed):
                continue
            sp_raw = row[idx["Story_Point"]]
            if sp_raw is None:
                continue
            try:
                sp_val = float(sp_raw)
            except (TypeError, ValueError):
                continue
            pid_raw = row[idx["Project_ID"]]
            if pid_raw is None:
                continue
            pid = int(pid_raw)
            iid = int(row[idx["ID"]])  # type: ignore[arg-type]
            ikey = str(row[idx["Issue_Key"]] or "")
            cdate = str(row[idx["Creation_Date"]] or "")
            title = row[idx["Title"]]
            desc = row[idx["Description"]]
            issues_by_pid.setdefault(pid, []).append((iid, ikey, cdate, sp_val, title, desc))

    if not proj_key_by_id:
        raise ValueError(f"No requested projects {sorted(target_set)} found in Project table of {sql_path}.")

    filtered_issues_by_proj: Dict[str, List[Tuple[int, str, str, float, Optional[str], Optional[str]]]] = {}
    issue_to_proj: Dict[int, str] = {}
    for pid, pkey in proj_key_by_id.items():
        rows = issues_by_pid.get(pid, [])
        filtered_issues_by_proj[pkey] = rows
        for r in rows:
            issue_to_proj[r[0]] = pkey
    issues_by_pid.clear()

    valid_issue_ids: Set[int] = set(issue_to_proj.keys())
    print(
        f"  ✓ Pass 1 complete: {len(filtered_issues_by_proj)} projects matched, "
        f"{len(valid_issue_ids)} issues with Story_Point."
    )

    print(f"🔎 [SQL Pass 2/2] Filtering Change_Log rows for target issues & fields ...")
    cl_by_proj: Dict[str, List[Tuple[int, int, str, Optional[str], Optional[str], str]]] = {
        p: [] for p in filtered_issues_by_proj
    }
    table_cols2, gen2 = _iter_table_inserts(sql_path, {"Change_Log"})
    # Seed column layout discovered in Pass 1 if available
    table_cols2["Change_Log"] = table_cols.get("Change_Log", table_cols2["Change_Log"])

    cl_kept = 0
    for _, explicit_cols, row in gen2:
        cols = explicit_cols or table_cols2["Change_Log"]
        idx = {c: pos for pos, c in enumerate(cols)}
        need = (idx["ID"], idx["Issue_ID"], idx["Field"], idx["From_String"], idx["To_String"], idx["Creation_Date"])
        if len(row) <= max(need):
            continue
        iid_raw = row[idx["Issue_ID"]]
        if iid_raw is None:
            continue
        try:
            iid = int(iid_raw)
        except (TypeError, ValueError):
            continue
        if iid not in valid_issue_ids:
            continue
        field_raw = row[idx["Field"]]
        if field_raw is None:
            continue
        field_str = str(field_raw)
        if field_str.lower() not in TARGET_CHANGELOG_FIELDS:
            continue
        cid = int(row[idx["ID"]])  # type: ignore[arg-type]
        pkey = issue_to_proj[iid]
        cl_by_proj[pkey].append(
            (
                cid,
                iid,
                field_str,
                row[idx["From_String"]],
                row[idx["To_String"]],
                str(row[idx["Creation_Date"]] or ""),
            )
        )
        cl_kept += 1

    print(f"  ✓ Pass 2 complete: kept {cl_kept} relevant Change_Log entries.")

    snapshots: Dict[str, pd.DataFrame] = {}
    for p in projects:
        p_up = p.upper()
        if p_up not in filtered_issues_by_proj:
            continue
        iss_df = pd.DataFrame(
            filtered_issues_by_proj[p_up],
            columns=["ID", "Issue_Key", "Creation_Date", "Story_Point", "Title", "Description"],
        )
        cl_df = pd.DataFrame(
            cl_by_proj[p_up],
            columns=["ID", "Issue_ID", "Field", "From_String", "To_String", "Creation_Date"],
        )
        snapshots[p_up] = build_snapshot(iss_df, cl_df)
    return snapshots


# ---------------------------------------------------------------------------
# Source Discovery & Extraction Helpers (MySQL / Interim / Existing Snapshot)
# ---------------------------------------------------------------------------

def _search_roots(input_dir: Optional[str]) -> List[str]:
    roots: List[str] = []
    for cand in (
        input_dir,
        os.path.join(REPO_ROOT, "data", "raw"),
        os.path.join(REPO_ROOT, "data", "interim"),
        os.path.join(REPO_ROOT, "data", "processed"),
        "/kaggle/input" if os.path.isdir("/kaggle/input") else None,
    ):
        if cand and os.path.exists(cand) and cand not in roots:
            roots.append(cand)
    return roots


def _find_sql_file(explicit_sql: Optional[str], input_dir: Optional[str]) -> Optional[str]:
    if explicit_sql and os.path.isfile(explicit_sql):
        return explicit_sql
    for root in _search_roots(input_dir):
        for pat in ("*.sql", "*.sql.gz", "*.sql.zip"):
            matches = sorted(glob.glob(os.path.join(root, "**", pat), recursive=True))
            tawos_first = [m for m in matches if "tawos" in os.path.basename(m).lower()]
            if tawos_first:
                return tawos_first[0]
            if matches:
                return matches[0]
    return None


def _find_project_pair(project: str, roots: Sequence[str], suffix_a: str, suffix_b: str) -> Optional[Tuple[str, str]]:
    a_low = f"{project.lower()}_{suffix_a}"
    b_low = f"{project.lower()}_{suffix_b}"
    found_a, found_b = None, None
    for root in roots:
        for path in sorted(glob.glob(os.path.join(root, "**", "*.parquet"), recursive=True)):
            base = os.path.basename(path).lower()
            if base == a_low and not found_a:
                found_a = path
            elif base == b_low and not found_b:
                found_b = path
            if found_a and found_b:
                return found_a, found_b
    return None


def _find_existing_snapshot(project: str, roots: Sequence[str]) -> Optional[str]:
    targets = {f"{project.lower()}_snapshot.parquet", f"{project.lower()}_snapshot.csv"}
    for root in roots:
        for ext in ("*.parquet", "*.csv"):
            for path in sorted(glob.glob(os.path.join(root, "**", ext), recursive=True)):
                if os.path.basename(path).lower() in targets:
                    return path
    return None


def _download_sql_if_needed(url: str, dest_dir: str) -> str:
    os.makedirs(dest_dir, exist_ok=True)
    fname = os.path.basename(url.split("?")[0]) or "TAWOS.sql"
    dest_path = os.path.join(dest_dir, fname)
    if os.path.isfile(dest_path) and os.path.getsize(dest_path) > 0:
        print(f"ℹ️ Using cached SQL download: {dest_path}")
        return dest_path
    print(f"⬇️ Downloading SQL dataset from {url} -> {dest_path} ...")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NCKH3-Research/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp, open(dest_path, "wb") as out:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
            return dest_path
        except Exception as exc:
            if attempt == 2:
                raise RuntimeError(f"Failed to download SQL archive from {url}: {exc}") from exc
            time.sleep(2 ** attempt)
    return dest_path


def _mysql_engine():
    try:
        from dotenv import load_dotenv

        env_path = os.path.join(REPO_ROOT, ".env")
        if os.path.isfile(env_path):
            load_dotenv(env_path)
    except ImportError:
        pass

    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL

    user = os.environ.get("MYSQL_USER")
    pwd = os.environ.get("MYSQL_PWD")
    db = os.environ.get("MYSQL_DB", "tawos")
    if not user or pwd is None:
        raise RuntimeError(
            "MySQL credentials missing. Set MYSQL_USER, MYSQL_PWD, MYSQL_DB in env or .env."
        )
    url = URL.create(
        "mysql+pymysql",
        username=user,
        password=pwd,
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=db,
    )
    return create_engine(url)


def compute_project_audit_row(project: str, snap_df: pd.DataFrame) -> Dict[str, Any]:
    """Compute leakage & chronological split audit stats matching Johnny's snapshot diagnostics."""
    n_snap = int(len(snap_df))
    no_label = int(snap_df["Story_Point"].isna().sum())
    pl_lt_cr = int((snap_df["Planning_Date"] < snap_df["Creation_Date"]).sum())
    pct_pl_gt = float((snap_df["Planning_Date"] > snap_df["Creation_Date"]).mean() * 100.0) if n_snap else 0.0

    sp = snap_df[["Story_Point", "Final_Story_Point"]]
    valid = snap_df[sp.notna().all(axis=1) & (sp.max(axis=1) <= MAX_SP)].sort_values(
        ["Planning_Date", "ID"]
    ).reset_index(drop=True)
    n_valid = int(len(valid))
    a = round(n_valid * SPLIT[0])
    b = round(n_valid * (SPLIT[0] + SPLIT[1]))
    n_train, n_val, n_test = int(a), int(max(0, b - a)), int(max(0, n_valid - b))

    sp_chg = valid["Story_Point"] != valid["Final_Story_Point"]
    ti_chg = valid["Title"].fillna("") != valid["Final_Title"].fillna("")
    de_chg = valid["Description"].fillna("") != valid["Final_Description"].fillna("")
    any_chg = sp_chg | ti_chg | de_chg

    return {
        "Project": project,
        "N_Snapshot": n_snap,
        "N_Valid_SP_LE100": n_valid,
        "N_Train": n_train,
        "N_Val": n_val,
        "N_Test": n_test,
        "Pct_Planning_GT_Created": round(pct_pl_gt, 2),
        "Pct_Changed_All": round(float(any_chg.mean() * 100.0), 2) if n_valid else 0.0,
        "Pct_SP_Changed": round(float(sp_chg.mean() * 100.0), 2) if n_valid else 0.0,
        "Pct_Title_Changed": round(float(ti_chg.mean() * 100.0), 2) if n_valid else 0.0,
        "Pct_Desc_Changed": round(float(de_chg.mean() * 100.0), 2) if n_valid else 0.0,
        "No_Label_Count": no_label,
        "Planning_LT_Created_Count": pl_lt_cr,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build, clean, audit, and publish TAWOS 13-project planning-time snapshots "
            "without requiring MySQL (supports TAWOS.sql(.gz/.zip), interim parquet, snapshot parquet/csv, or MySQL)."
        )
    )
    parser.add_argument(
        "--source",
        type=str,
        default="auto",
        choices=["auto", "sql", "mysql", "interim", "snapshot"],
        help="Input source mode (default: auto).",
    )
    parser.add_argument("--sql-path", type=str, default=None, help="Path to TAWOS.sql / .sql.gz / .sql.zip")
    parser.add_argument("--download-url", type=str, default=None, help="Optional URL to download TAWOS.sql archive")
    parser.add_argument("--input-dir", type=str, default=None, help="Directory holding SQL, interim, or snapshot files")
    parser.add_argument("--output-dir", type=str, default=None, help="Directory to save <PROJECT>_snapshot.parquet files")
    parser.add_argument("--projects", type=str, default="all", help="'all' or comma-separated TAWOS project keys")
    parser.add_argument("--results-repo", type=str, default=DEFAULT_RESULTS_REPO_NAME)
    parser.add_argument("--remote-subdir", type=str, default=DEFAULT_SNAPSHOTS_SUBDIR)
    parser.add_argument("--private-hf", action="store_true")
    parser.add_argument("--no-hf-push", action="store_true")
    return parser.parse_args()


def resolve_source_mode(args: argparse.Namespace) -> Tuple[str, Optional[str]]:
    """Determine concrete source type and optional sql_path when --source auto is used."""
    out_dir = resolve_data_dir(args.output_dir)
    sql_path = args.sql_path
    if args.download_url and (not sql_path or not os.path.isfile(sql_path)):
        sql_path = _download_sql_if_needed(args.download_url, os.path.join(out_dir, "_downloads"))

    if args.source != "auto":
        return args.source, sql_path

    detected_sql = _find_sql_file(sql_path, args.input_dir)
    if detected_sql:
        return "sql", detected_sql

    roots = _search_roots(args.input_dir)
    if _find_project_pair("BAM", roots, "issue.parquet", "changelog.parquet"):
        return "interim", None
    if _find_existing_snapshot("BAM", roots):
        return "snapshot", None
    if os.environ.get("MYSQL_USER") and os.environ.get("MYSQL_PWD") is not None:
        return "mysql", None

    raise FileNotFoundError(
        "Could not auto-detect any TAWOS source. Provide one of:\n"
        "  • --sql-path <path/to/TAWOS.sql(.gz/.zip)>\n"
        "  • --input-dir <dir with <PROJECT>_{issue,changelog}.parquet or <PROJECT>_snapshot.parquet>\n"
        "  • --source mysql with MYSQL_USER / MYSQL_PWD / MYSQL_DB configured"
    )


def main() -> None:
    args = parse_args()
    projects = parse_projects_arg(args.projects)
    out_dir = resolve_data_dir(args.output_dir)
    roots = _search_roots(args.input_dir)

    mode, sql_path = resolve_source_mode(args)
    print("=" * 85)
    print(f"🛠️ TAWOS DATASET PREPARATION | source={mode} | projects={len(projects)} | out={out_dir}")
    print("=" * 85)

    snapshots: Dict[str, pd.DataFrame] = {}
    if mode == "sql":
        final_sql = sql_path or _find_sql_file(None, args.input_dir)
        if not final_sql or not os.path.isfile(final_sql):
            raise FileNotFoundError(f"SQL file not found: {final_sql}")
        snapshots = build_snapshots_from_sql(final_sql, projects)
    elif mode == "interim":
        for p in projects:
            pair = _find_project_pair(p, roots, "issue.parquet", "changelog.parquet")
            if not pair:
                raise FileNotFoundError(f"Interim parquets (<PROJECT>_issue.parquet & _changelog.parquet) missing for {p}")
            iss_df = pd.read_parquet(pair[0])
            cl_df = pd.read_parquet(pair[1])
            snapshots[p] = build_snapshot(iss_df, cl_df)
    elif mode == "snapshot":
        for p in projects:
            src_path = _find_existing_snapshot(p, roots)
            if not src_path:
                raise FileNotFoundError(f"Existing snapshot parquet/csv missing for {p} in {roots}")
            raw_df = pd.read_parquet(src_path) if src_path.lower().endswith(".parquet") else pd.read_csv(src_path)
            snapshots[p] = normalize_existing_snapshot(raw_df, p)
    elif mode == "mysql":
        from sqlalchemy import text

        eng = _mysql_engine()
        with eng.connect() as conn:
            for p in projects:
                iss_df = pd.read_sql(text(MYSQL_SQL["issue"]), conn, params={"key": p})
                cl_df = pd.read_sql(text(MYSQL_SQL["changelog"]), conn, params={"key": p})
                snapshots[p] = build_snapshot(iss_df, cl_df)

    audit_rows: List[Dict[str, Any]] = []
    batch_items: List[Tuple[str, str]] = []

    for p in projects:
        if p not in snapshots:
            continue
        snap_df = snapshots[p]
        out_path = os.path.join(out_dir, f"{p}_snapshot.parquet")
        snap_df.to_parquet(out_path, index=False)
        batch_items.append((out_path, f"{p}_snapshot.parquet"))

        row = compute_project_audit_row(p, snap_df)
        audit_rows.append(row)
        print(
            f"  ✓ {p:10s} n={row['N_Snapshot']:6d}  valid(SP<=100)={row['N_Valid_SP_LE100']:6d}  "
            f"changed={row['Pct_Changed_All']:5.1f}%  sp_chg={row['Pct_SP_Changed']:4.1f}%  "
            f"pl<cr={row['Planning_LT_Created_Count']}"
        )

    summary_df = pd.DataFrame(audit_rows)
    summary_path = os.path.join(out_dir, "dataset_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    batch_items.append((summary_path, "dataset_summary.csv"))

    logger = HFExperimentLogger(
        results_repo_name=args.results_repo,
        checkpoints_repo_name=None,
        run_prefix=args.remote_subdir,
        enabled=not args.no_hf_push,
        private=args.private_hf,
    )
    meta_path = logger.write_and_upload_metadata(
        out_dir,
        vars(args),
        extra_info={
            "source_mode": mode,
            "n_projects": len(audit_rows),
            "total_valid_issues": int(summary_df["N_Valid_SP_LE100"].sum()) if not summary_df.empty else 0,
        },
        upload=False,
    )
    batch_items.append((meta_path, "metadata.json"))

    if logger.enabled:
        ok = logger.upload_results_batch(
            batch_items,
            f"Publish TAWOS snapshots ({mode}, {len(audit_rows)} projects)",
        )
        if ok:
            print(f"\n✅ Published {len(batch_items)} files to {logger.results_repo_id}/{args.remote_subdir} in 1 commit!")
    else:
        print(f"\nℹ️ Snapshots ready locally in {out_dir}")


if __name__ == "__main__":
    main()
