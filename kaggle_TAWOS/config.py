"""Central configuration for TAWOS Planning-Time Snapshot experiments (ported from SR-G3_planning-time-sp)."""

import glob
import os
from typing import Dict, List, Optional, Sequence, Tuple

GITHUB_REPO_URL = "https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake.git"
SOURCE_REFERENCE_REPO = "https://github.com/JohnnyPhan1712/SR-G3_planning-time-sp.git"

DEFAULT_RESULTS_REPO_NAME = "NCKH3-StoryPoint-Artifact"
DEFAULT_CHECKPOINTS_REPO_NAME = "NCKH3-StoryPoint-Checkpoints"
DEFAULT_SNAPSHOTS_SUBDIR = "datasets/tawos_snapshots"

SEED = 42
SPLIT: Tuple[float, float, float] = (0.6, 0.2, 0.2)
MAX_SP = 100

# 13 TAWOS V1.1 projects overlapping with the Deep-SE benchmark
PROJECTS: List[str] = [
    "APSTUD",
    "BAM",
    "CLOV",
    "DM",
    "DURACLOUD",
    "JSWSERVER",
    "MDL",
    "MESOS",
    "MULE",
    "TIMOB",
    "TISTUD",
    "USERGRID",
    "XD",
]

TAWOS_TO_DEEPSE: Dict[str, str] = {
    "APSTUD": "aptanastudio",
    "BAM": "bamboo",
    "CLOV": "clover",
    "DM": "datamanagement",
    "DURACLOUD": "duracloud",
    "JSWSERVER": "jirasoftware",
    "MDL": "moodle",
    "MESOS": "mesos",
    "MULE": "mule",
    "TIMOB": "titanium",
    "TISTUD": "appceleratorstudio",
    "USERGRID": "usergrid",
    "XD": "springxd",
}

DEEPSE_TO_TAWOS: Dict[str, str] = {v: k for k, v in TAWOS_TO_DEEPSE.items()}

# Lowercased Change_Log.Field names holding the estimate.
# Excludes 'Actual Story Points' (XD, set on close) and 'Epic Story Progress' (DM).
SP_FIELDS = {"story points", "story points (obsolete)"}
TEXT_FIELDS: Dict[str, str] = {"summary": "Title", "description": "Description"}

SNAPSHOT_REQUIRED_COLS: List[str] = [
    "ID",
    "Issue_Key",
    "Creation_Date",
    "Planning_Date",
    "Story_Point",
    "Final_Story_Point",
    "Title",
    "Final_Title",
    "Description",
    "Final_Description",
]

PREDICTION_COLS: List[str] = [
    "project",
    "ID",
    "Issue_Key",
    "Planning_Date",
    "changed",
    "Story_Point",
    "Final_Story_Point",
    "y_true",
    "y_pred",
]

# setting -> (train/val text col, train/val label col, test text col, test label col)
SETTINGS: Dict[str, Tuple[str, str, str, str]] = {
    "final": ("Final_Text", "Final_Story_Point", "Final_Text", "Final_Story_Point"),
    "planning": ("Text", "Story_Point", "Text", "Story_Point"),
    "cross": ("Final_Text", "Final_Story_Point", "Text", "Story_Point"),
}


def resolve_output_dir(explicit_dir: Optional[str], default_subdir: str) -> str:
    """Resolve output directory based on explicit flag or Kaggle/local runtime."""
    norm_sub = os.path.normpath(default_subdir.strip("/\\"))
    if explicit_dir:
        out_dir = explicit_dir
    elif os.path.exists("/kaggle/working"):
        out_dir = os.path.join("/kaggle/working", "outputs", norm_sub)
    else:
        out_dir = os.path.join("kaggle_TAWOS", "outputs", norm_sub)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def resolve_data_dir(explicit_dir: Optional[str] = None) -> str:
    """Resolve snapshot cache directory for Kaggle or local runs."""
    if explicit_dir:
        data_dir = explicit_dir
    elif os.path.exists("/kaggle/working"):
        data_dir = os.path.join("/kaggle/working", "data", "tawos_snapshots")
    else:
        data_dir = os.path.join("kaggle_TAWOS", "outputs", "tawos_snapshots")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def discover_snapshot_file(project: str, search_dirs: Sequence[str] = ()) -> Optional[str]:
    """Locate `<PROJECT>_snapshot.parquet` in explicit search dirs, /kaggle/input, or local defaults."""
    proj_upper = project.strip().upper()
    candidate_names = [
        f"{proj_upper}_snapshot.parquet",
        f"{proj_upper.lower()}_snapshot.parquet",
        f"{project.strip()}_snapshot.parquet",
    ]
    target_lower = f"{proj_upper.lower()}_snapshot.parquet"

    dirs_to_check: List[str] = []
    for d in search_dirs:
        if d and os.path.isdir(d):
            dirs_to_check.append(d)
            nested_ds = os.path.join(d, "datasets", "tawos_snapshots")
            if os.path.isdir(nested_ds):
                dirs_to_check.append(nested_ds)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fallback_dir in (
        os.path.join(repo_root, "data", "processed"),
        resolve_data_dir(None),
    ):
        if os.path.isdir(fallback_dir) and fallback_dir not in dirs_to_check:
            dirs_to_check.append(fallback_dir)

    for base_dir in dirs_to_check:
        for cname in candidate_names:
            cand = os.path.join(base_dir, cname)
            if os.path.isfile(cand) and os.path.getsize(cand) > 0:
                return cand
        try:
            for entry in os.listdir(base_dir):
                if entry.lower() == target_lower:
                    cand = os.path.join(base_dir, entry)
                    if os.path.isfile(cand) and os.path.getsize(cand) > 0:
                        return cand
        except OSError:
            pass

    if os.path.isdir("/kaggle/input"):
        for match in sorted(glob.glob(os.path.join("/kaggle/input", "**", "*_snapshot.parquet"), recursive=True)):
            if os.path.basename(match).lower() == target_lower and os.path.getsize(match) > 0:
                return match

    return None


def parse_projects_arg(raw: str) -> List[str]:
    """Parse '--projects all' or comma-separated TAWOS project keys (case-insensitive)."""
    if not raw or raw.strip().lower() == "all":
        return list(PROJECTS)

    canon = {p.upper(): p for p in PROJECTS}
    selected: List[str] = []
    unknown: List[str] = []
    for item in raw.split(","):
        key = item.strip()
        if not key:
            continue
        upper = key.upper()
        if upper in canon:
            proj = canon[upper]
        elif key.lower() in DEEPSE_TO_TAWOS:
            proj = DEEPSE_TO_TAWOS[key.lower()]
        else:
            unknown.append(key)
            continue
        if proj not in selected:
            selected.append(proj)

    if unknown:
        valid = ", ".join(PROJECTS)
        raise ValueError(f"Unknown TAWOS project(s): {unknown}. Valid projects: {valid}")
    return selected
