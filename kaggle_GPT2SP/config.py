"""Central configuration and published benchmark tables for NCKH 3 experiments."""

import os
import time
import urllib.request
from typing import Dict, List, Optional, Tuple
import pandas as pd

GITHUB_REPO_URL = "https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake.git"
GPT2SP_DATA_BASE_URL = (
    "https://raw.githubusercontent.com/awsm-research/gpt2sp/main/sp_dataset/marked_data/"
)

DEFAULT_RESULTS_REPO_NAME = "NCKH_GPT2SP"
DEFAULT_CHECKPOINTS_REPO_NAME = "nckh3-gpt2sp-checkpoints"

# Ground-truth values extracted from:
# - Fu & Tantithamthavorn (IEEE TSE 2023, Table 4 & within_proj_data.csv)
# - Choetkiertikul et al. (IEEE TSE 2019, Table II)
BENCHMARK_PROJECTS = {
    "appceleratorstudio": {
        "abbr": "AS",
        "name": "Appcelerator Studio",
        "reported_gpt2sp": 0.84,
        "reported_deepse": 1.36,
        "reported_deepse_in_gpt2sp": 1.36,
        "reported_deepse_sa": 60.26,
        "rep_median": 1.84,
        "rep_mean": 2.08,
    },
    "aptanastudio": {
        "abbr": "AP",
        "name": "Aptana Studio",
        "reported_gpt2sp": 1.93,
        "reported_deepse": 2.71,
        "reported_deepse_in_gpt2sp": 2.71,
        "reported_deepse_sa": 42.58,
        "rep_median": 3.71,
        "rep_mean": 3.15,
    },
    "bamboo": {
        "abbr": "BB",
        "name": "Bamboo",
        "reported_gpt2sp": 0.44,
        "reported_deepse": 0.74,
        "reported_deepse_in_gpt2sp": 0.74,
        "reported_deepse_sa": 71.24,
        "rep_median": 1.32,
        "rep_mean": 1.75,
    },
    "clover": {
        "abbr": "CV",
        "name": "Clover",
        "reported_gpt2sp": 1.98,
        "reported_deepse": 2.11,
        "reported_deepse_in_gpt2sp": 2.11,
        "reported_deepse_sa": 50.45,
        "rep_median": 2.84,
        "rep_mean": 3.49,
    },
    "datamanagement": {
        "abbr": "DM",
        "name": "Data Management",
        "reported_gpt2sp": 3.10,
        "reported_deepse": 3.77,
        "reported_deepse_in_gpt2sp": 3.77,
        "reported_deepse_sa": 47.87,
        "rep_median": 4.82,
        "rep_mean": 5.29,
    },
    "duracloud": {
        "abbr": "DC",
        "name": "DuraCloud",
        "reported_gpt2sp": 0.48,
        "reported_deepse": 0.68,
        "reported_deepse_in_gpt2sp": 0.68,
        "reported_deepse_sa": 69.92,
        "rep_median": 0.73,
        "rep_mean": 1.30,
    },
    "jirasoftware": {
        "abbr": "JI",
        "name": "Jira Software",
        "reported_gpt2sp": 0.92,
        "reported_deepse": 1.38,
        "reported_deepse_in_gpt2sp": 1.38,
        "reported_deepse_sa": 59.52,
        "rep_median": 2.93,
        "rep_mean": 2.48,
    },
    "mesos": {
        "abbr": "ME",
        "name": "Mesos",
        "reported_gpt2sp": 0.66,
        "reported_deepse": 1.02,
        "reported_deepse_in_gpt2sp": 1.02,
        "reported_deepse_sa": 59.03,
        "rep_median": 1.73,
        "rep_mean": 1.64,
    },
    "moodle": {
        "abbr": "MD",
        "name": "Moodle",
        "reported_gpt2sp": 4.09,
        "reported_deepse": 5.97,
        "reported_deepse_in_gpt2sp": 5.97,
        "reported_deepse_sa": 50.29,
        "rep_median": 7.18,
        "rep_mean": 10.90,
    },
    "mule": {
        "abbr": "MU",
        "name": "Mule",
        "reported_gpt2sp": 1.43,
        "reported_deepse": 2.18,
        "reported_deepse_in_gpt2sp": 2.18,
        "reported_deepse_sa": 40.09,
        "rep_median": 2.69,
        "rep_mean": 2.59,
    },
    "mulestudio": {
        "abbr": "MS",
        "name": "Mule Studio",
        "reported_gpt2sp": 2.04,
        "reported_deepse": 3.23,
        "reported_deepse_in_gpt2sp": 3.23,
        "reported_deepse_sa": 17.17,
        "rep_median": 3.30,
        "rep_mean": 3.34,
    },
    "springxd": {
        "abbr": "XD",
        "name": "Spring XD",
        "reported_gpt2sp": 0.96,
        "reported_deepse": 1.63,
        "reported_deepse_in_gpt2sp": 1.61,
        "reported_deepse_sa": 46.82,
        "rep_median": 2.07,
        "rep_mean": 2.27,
    },
    "talenddataquality": {
        "abbr": "TD",
        "name": "Talend Data Quality",
        "reported_gpt2sp": 1.58,
        "reported_deepse": 2.97,
        "reported_deepse_in_gpt2sp": 2.97,
        "reported_deepse_sa": 48.28,
        "rep_median": 3.87,
        "rep_mean": 4.81,
    },
    "talendesb": {
        "abbr": "TE",
        "name": "Talend ESB",
        "reported_gpt2sp": 0.50,
        "reported_deepse": 0.64,
        "reported_deepse_in_gpt2sp": 0.64,
        "reported_deepse_sa": 69.67,
        "rep_median": 1.16,
        "rep_mean": 1.14,
    },
    "titanium": {
        "abbr": "TI",
        "name": "Titanium",
        "reported_gpt2sp": 1.36,
        "reported_deepse": 1.97,
        "reported_deepse_in_gpt2sp": 1.97,
        "reported_deepse_sa": 55.92,
        "rep_median": 2.47,
        "rep_mean": 3.05,
    },
    "usergrid": {
        "abbr": "UG",
        "name": "Usergrid",
        "reported_gpt2sp": 0.68,
        "reported_deepse": 1.03,
        "reported_deepse_in_gpt2sp": 1.03,
        "reported_deepse_sa": 52.66,
        "rep_median": 1.60,
        "rep_mean": 1.48,
    },
}


def resolve_output_dir(explicit_dir: str, default_subdir: str) -> str:
    """Resolve output directory based on explicit flag or Kaggle/local runtime."""
    if explicit_dir:
        out_dir = explicit_dir
    elif os.path.exists("/kaggle/working"):
        out_dir = os.path.join("/kaggle/working", "outputs", default_subdir)
    else:
        out_dir = os.path.join("kaggle_GPT2SP", "outputs", default_subdir)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def parse_projects_arg(projects_arg: str) -> List[str]:
    """Parse '--projects all' or comma-separated project keys into validated names."""
    if not projects_arg or projects_arg.strip().lower() == "all":
        return list(BENCHMARK_PROJECTS.keys())
    selected = [p.strip().lower() for p in projects_arg.split(",") if p.strip()]
    unknown = [p for p in selected if p not in BENCHMARK_PROJECTS]
    if unknown:
        valid = ", ".join(BENCHMARK_PROJECTS.keys())
        raise ValueError(f"Unknown project(s): {unknown}. Valid projects: {valid}")
    return selected


def download_file_with_retry(url: str, local_path: str, retries: int = 3) -> str:
    """Download a file to local_path if not already cached, retrying on transient failures."""
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return local_path
    os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NCKH3-Research/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp, open(local_path, "wb") as out:
                out.write(resp.read())
            return local_path
        except Exception as exc:
            if attempt == retries - 1:
                raise RuntimeError(f"Failed downloading {url}: {exc}") from exc
            time.sleep(2 ** attempt)
    return local_path


def load_gpt2sp_splits(project_name: str, cache_dir: str) -> Dict[str, pd.DataFrame]:
    """Load marked CSV from awsm-research/gpt2sp and return train/val/test DataFrames."""
    csv_path = os.path.join(cache_dir, f"{project_name}_gpt2sp.csv")
    download_file_with_retry(f"{GPT2SP_DATA_BASE_URL}{project_name}.csv", csv_path)
    df = pd.read_csv(csv_path)

    if "split_mark" in df.columns:
        marks = df["split_mark"].astype(str).str.lower()
        return {
            "train": df[marks == "train"].reset_index(drop=True),
            "val": df[marks.isin(["val", "valid", "validation"])].reset_index(drop=True),
            "test": df[marks == "test"].reset_index(drop=True),
            "all": df,
        }

    n = len(df)
    n_train = int(n * 0.6)
    n_val_end = int(n * 0.8)
    return {
        "train": df.iloc[:n_train].reset_index(drop=True),
        "val": df.iloc[n_train:n_val_end].reset_index(drop=True),
        "test": df.iloc[n_val_end:].reset_index(drop=True),
        "all": df,
    }


def format_issue_texts(df: pd.DataFrame, include_description: bool = False) -> List[str]:
    """Build input text list cleanly, avoiding Future Information Leakage when needed."""
    title_col = "title" if "title" in df.columns else "Title"
    titles = df[title_col].fillna("").astype(str)
    if not include_description:
        return titles.tolist()
    desc_col = "description" if "description" in df.columns else "Description"
    if desc_col not in df.columns:
        return titles.tolist()
    descs = df[desc_col].fillna("").astype(str)
    return (titles + " " + descs).str.strip().tolist()


