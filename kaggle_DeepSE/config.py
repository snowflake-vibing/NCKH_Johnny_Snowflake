"""Central configuration, benchmark tables, and data loaders for Deep-SE experiments."""

import gzip
import os
import pickle
import time
import urllib.request
import warnings
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

GITHUB_REPO_URL = "https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake.git"
DEEPSE_BASE_URL = (
    "https://raw.githubusercontent.com/morakotch/datasets/master/"
    "storypoint/IEEE%20TSE2018/Deep-SE/"
)
DEEPSE_DATA_BASE_URL = DEEPSE_BASE_URL + "data/"
DEEPSE_PRETRAIN_BASE_URL = DEEPSE_BASE_URL + "NCE/bestModels/"

DEFAULT_RESULTS_REPO_NAME = "NCKH3-StoryPoint-Artifact"
DEFAULT_CHECKPOINTS_REPO_NAME = "NCKH3-StoryPoint-Checkpoints"

# Ground-truth values & repository mapping extracted from:
# - Choetkiertikul et al. (IEEE TSE 2019, Table II)
# - morakotch/datasets/storypoint/IEEE TSE2018/Deep-SE/classification/exp_script.py
BENCHMARK_PROJECTS: Dict[str, Dict[str, Any]] = {
    "appceleratorstudio": {
        "abbr": "AS",
        "name": "Appcelerator Studio",
        "repo": "appcelerator",
        "reported_deepse": 1.36,
        "reported_deepse_sa": 60.26,
        "rep_median": 1.84,
        "rep_mean": 2.08,
    },
    "aptanastudio": {
        "abbr": "AP",
        "name": "Aptana Studio",
        "repo": "appcelerator",
        "reported_deepse": 2.71,
        "reported_deepse_sa": 42.58,
        "rep_median": 3.71,
        "rep_mean": 3.15,
    },
    "bamboo": {
        "abbr": "BB",
        "name": "Bamboo",
        "repo": "jira",
        "reported_deepse": 0.74,
        "reported_deepse_sa": 71.24,
        "rep_median": 1.32,
        "rep_mean": 1.75,
    },
    "clover": {
        "abbr": "CV",
        "name": "Clover",
        "repo": "jira",
        "reported_deepse": 2.11,
        "reported_deepse_sa": 50.45,
        "rep_median": 2.84,
        "rep_mean": 3.49,
    },
    "datamanagement": {
        "abbr": "DM",
        "name": "Data Management",
        "repo": "lsstcorp",
        "reported_deepse": 3.77,
        "reported_deepse_sa": 47.87,
        "rep_median": 4.82,
        "rep_mean": 5.29,
    },
    "duracloud": {
        "abbr": "DC",
        "name": "DuraCloud",
        "repo": "duraspace",
        "reported_deepse": 0.68,
        "reported_deepse_sa": 69.92,
        "rep_median": 0.73,
        "rep_mean": 1.30,
    },
    "jirasoftware": {
        "abbr": "JI",
        "name": "Jira Software",
        "repo": "jira",
        "reported_deepse": 1.38,
        "reported_deepse_sa": 59.52,
        "rep_median": 2.93,
        "rep_mean": 2.48,
    },
    "mesos": {
        "abbr": "ME",
        "name": "Mesos",
        "repo": "apache",
        "reported_deepse": 1.02,
        "reported_deepse_sa": 59.03,
        "rep_median": 1.73,
        "rep_mean": 1.64,
    },
    "moodle": {
        "abbr": "MD",
        "name": "Moodle",
        "repo": "moodle",
        "reported_deepse": 5.97,
        "reported_deepse_sa": 50.29,
        "rep_median": 7.18,
        "rep_mean": 10.90,
    },
    "mule": {
        "abbr": "MU",
        "name": "Mule",
        "repo": "mulesoft",
        "reported_deepse": 2.18,
        "reported_deepse_sa": 40.09,
        "rep_median": 2.69,
        "rep_mean": 2.59,
    },
    "mulestudio": {
        "abbr": "MS",
        "name": "Mule Studio",
        "repo": "mulesoft",
        "reported_deepse": 3.23,
        "reported_deepse_sa": 17.17,
        "rep_median": 3.30,
        "rep_mean": 3.34,
    },
    "springxd": {
        "abbr": "XD",
        "name": "Spring XD",
        "repo": "spring",
        "reported_deepse": 1.63,
        "reported_deepse_sa": 46.82,
        "rep_median": 2.07,
        "rep_mean": 2.27,
    },
    "talenddataquality": {
        "abbr": "TD",
        "name": "Talend Data Quality",
        "repo": "talendforge",
        "reported_deepse": 2.97,
        "reported_deepse_sa": 48.28,
        "rep_median": 3.87,
        "rep_mean": 4.81,
    },
    "talendesb": {
        "abbr": "TE",
        "name": "Talend ESB",
        "repo": "talendforge",
        "reported_deepse": 0.64,
        "reported_deepse_sa": 69.67,
        "rep_median": 1.16,
        "rep_mean": 1.14,
    },
    "titanium": {
        "abbr": "TI",
        "name": "Titanium",
        "repo": "appcelerator",
        "reported_deepse": 1.97,
        "reported_deepse_sa": 55.92,
        "rep_median": 2.47,
        "rep_mean": 3.05,
    },
    "usergrid": {
        "abbr": "UG",
        "name": "Usergrid",
        "repo": "apache",
        "reported_deepse": 1.03,
        "reported_deepse_sa": 52.66,
        "rep_median": 1.60,
        "rep_mean": 1.48,
    },
}


def resolve_output_dir(explicit_dir: Optional[str], default_subdir: str) -> str:
    """Resolve output directory based on explicit flag or Kaggle/local runtime."""
    norm_sub = os.path.normpath(default_subdir.strip("/\\"))
    if explicit_dir:
        out_dir = explicit_dir
    elif os.path.exists("/kaggle/working"):
        out_dir = os.path.join("/kaggle/working", "outputs", norm_sub)
    else:
        out_dir = os.path.join("kaggle_DeepSE", "outputs", norm_sub)
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


def load_deepse_splits(project_name: str, cache_dir: str) -> Dict[str, pd.DataFrame]:
    """Load raw CSV and _3sets.txt split matrix from morakotch/datasets."""
    csv_path = os.path.join(cache_dir, f"{project_name}_deepse.csv")
    sets_path = os.path.join(cache_dir, f"{project_name}_3sets.txt")
    download_file_with_retry(f"{DEEPSE_DATA_BASE_URL}{project_name}.csv", csv_path)
    download_file_with_retry(f"{DEEPSE_DATA_BASE_URL}{project_name}_3sets.txt", sets_path)

    df = pd.read_csv(csv_path)
    sets = pd.read_csv(sets_path, sep=r"\s+")
    return {
        "train": df.loc[sets["train"] == 1].reset_index(drop=True),
        "val": df.loc[sets["valid"] == 1].reset_index(drop=True),
        "test": df.loc[sets["test"] == 1].reset_index(drop=True),
        "all": df,
    }


def load_deepse_pkl_splits(project_name: str, cache_dir: str) -> Dict[str, Any]:
    """Download and unpickle author's preprocessed <project>.pkl.gz split tuple."""
    pkl_path = os.path.join(cache_dir, f"{project_name}.pkl.gz")
    download_file_with_retry(f"{DEEPSE_DATA_BASE_URL}{project_name}.pkl.gz", pkl_path)

    with gzip.open(pkl_path, "rb") as gz:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            data_tuple = pickle.load(gz, encoding="latin1")

    if len(data_tuple) != 9:
        raise ValueError(f"Unexpected tuple length {len(data_tuple)} in {pkl_path}")

    train_t, train_d, train_y, val_t, val_d, val_y, test_t, test_d, test_y = data_tuple
    return {
        "train_t": train_t,
        "train_d": train_d,
        "train_y": np.asarray(train_y, dtype=np.float32),
        "val_t": val_t,
        "val_d": val_d,
        "val_y": np.asarray(val_y, dtype=np.float32),
        "test_t": test_t,
        "test_d": test_d,
        "test_y": np.asarray(test_y, dtype=np.float32),
    }


def load_deepse_dict(repo_name: str, cache_dir: str) -> Dict[str, int]:
    """Download and unpickle repository vocabulary dict (<repo>.dict.pkl.gz)."""
    dict_path = os.path.join(cache_dir, f"{repo_name}.dict.pkl.gz")
    download_file_with_retry(f"{DEEPSE_DATA_BASE_URL}{repo_name}.dict.pkl.gz", dict_path)

    with gzip.open(dict_path, "rb") as gz:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            raw_dict = pickle.load(gz, encoding="latin1")

    return {str(k): int(v) for k, v in raw_dict.items()}


def build_vocab_from_texts(texts: Sequence[str]) -> Dict[str, int]:
    """Build frequency-ordered word dictionary on train text only (index 0 reserved for UNK)."""
    wordcount: Dict[str, int] = {}
    for ss in texts:
        words = (ss or "").strip().lower().split()
        for w in words:
            if w == "<unk>":
                continue
            wordcount[w] = wordcount.get(w, 0) + 1
    sorted_words = sorted(wordcount.keys(), key=lambda w: (-wordcount[w], w))
    return {w: idx + 1 for idx, w in enumerate(sorted_words)}


def texts_to_word_ids(texts: Sequence[str], dictionary: Dict[str, int]) -> List[List[int]]:
    """Port of Deep-SE NCE/preprocess.py grab_data(): map whitespace tokens to dictionary IDs."""
    seqs: List[List[int]] = []
    for ss in texts:
        words = (ss or "").strip().lower().split()
        seqs.append([dictionary[w] if w in dictionary else 0 for w in words])
    return seqs


def prepare_sequence_tensors(
    title_seqs: Sequence[Sequence[int]],
    descr_seqs: Sequence[Sequence[int]],
    vocab_size: int = 500,
    max_len: int = 100,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Port of Deep-SE prepare_data.py: filter < vocab_size, shift +1 (0=PAD), build masks."""

    def create_mask(seqs: Sequence[Sequence[int]]) -> Tuple[np.ndarray, np.ndarray]:
        filtered = []
        for s in seqs:
            new_s = [int(w) for w in s if 0 <= int(w) < vocab_size]
            if len(new_s) == 0:
                new_s = [0]
            filtered.append(new_s)

        n_samples = len(filtered)
        x = np.zeros((n_samples, max_len), dtype=np.int64)
        mask = np.zeros((n_samples, max_len), dtype=np.float32)

        for i, s in enumerate(filtered):
            seq_len = min(max_len, len(s))
            mask[i, :seq_len] = 1.0
            x[i, :seq_len] = np.asarray(s[:seq_len], dtype=np.int64) + 1

        return x, mask

    title_x, title_mask = create_mask(title_seqs)
    descr_x, descr_mask = create_mask(descr_seqs)
    return title_x, title_mask, descr_x, descr_mask
