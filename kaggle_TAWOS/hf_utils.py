"""Hugging Face Hub integration for Secrets auth, auto-resume, checkpoints, snapshots, and results."""

from datetime import datetime, timezone
import json
import os
import subprocess
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple
from huggingface_hub import CommitOperationAdd, HfApi, hf_hub_download

try:
    from kaggle_TAWOS.config import (
        DEFAULT_RESULTS_REPO_NAME,
        DEFAULT_SNAPSHOTS_SUBDIR,
        discover_snapshot_file,
    )
except ImportError:
    from config import (  # type: ignore
        DEFAULT_RESULTS_REPO_NAME,
        DEFAULT_SNAPSHOTS_SUBDIR,
        discover_snapshot_file,
    )


def resolve_hf_token(explicit_token: Optional[str] = None) -> Optional[str]:
    """Resolve HF write token from argument, environment variables, or Kaggle Secrets."""
    if explicit_token and explicit_token.strip():
        return explicit_token.strip()

    for env_key in ("HF_TOKEN", "hf_token", "HUGGINGFACE_HUB_TOKEN"):
        val = os.environ.get(env_key)
        if val and val.strip():
            return val.strip()

    try:
        from kaggle_secrets import UserSecretsClient  # type: ignore

        client = UserSecretsClient()
        for secret_key in ("HF_TOKEN", "hf_token"):
            try:
                val = client.get_secret(secret_key)
                if val and val.strip():
                    return val.strip()
            except Exception:
                continue
    except ImportError:
        pass
    except Exception:
        pass

    return None


def get_git_info() -> Dict[str, str]:
    """Safely inspect current git branch and commit hash without failing outside git."""
    info = {"git_branch": "unknown", "git_commit": "unknown"}
    commands = {
        "git_branch": ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        "git_commit": ["git", "rev-parse", "HEAD"],
    }
    for key, cmd in commands.items():
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
            if out:
                info[key] = out
        except Exception:
            pass
    return info


class HFExperimentLogger:
    """Manages incremental uploads and resume checks with Hugging Face Dataset/Model repos."""

    def __init__(
        self,
        results_repo_name: str,
        checkpoints_repo_name: Optional[str] = None,
        run_prefix: str = "default_run",
        enabled: bool = True,
        private: bool = False,
        token: Optional[str] = None,
    ):
        self.run_prefix = run_prefix.strip("/")
        self.private = private
        self.enabled = False
        self.token: Optional[str] = None
        self.api: Optional[HfApi] = None
        self.username: Optional[str] = None
        self.results_repo_id: Optional[str] = None
        self.checkpoints_repo_id: Optional[str] = None

        if not enabled:
            print("ℹ️ HF push disabled (--no-hf-push). Results will be saved locally only.")
            return

        resolved_token = resolve_hf_token(token)
        if not resolved_token:
            print(
                "⚠️ No HF token found in env (HF_TOKEN/hf_token) or Kaggle Secrets. "
                "Continuing locally without HF upload."
            )
            return

        try:
            api = HfApi(token=resolved_token)
            who = api.whoami()
            username = who["name"]
        except Exception as exc:
            print(f"⚠️ Hugging Face authentication failed ({exc}). Continuing locally.")
            return

        self.token = resolved_token
        self.api = api
        self.username = username
        self.results_repo_id = self._qualify_repo(results_repo_name)
        try:
            self.api.create_repo(
                repo_id=self.results_repo_id,
                repo_type="dataset",
                private=self.private,
                exist_ok=True,
            )
            if checkpoints_repo_name:
                self.checkpoints_repo_id = self._qualify_repo(checkpoints_repo_name)
                self.api.create_repo(
                    repo_id=self.checkpoints_repo_id,
                    repo_type="model",
                    private=self.private,
                    exist_ok=True,
                )
        except Exception as exc:
            print(
                f"⚠️ Failed to create/access Hugging Face repo ({exc}). "
                "Please ensure HF_TOKEN/hf_token has WRITE permission. "
                "Continuing locally without HF upload."
            )
            self.enabled = False
            self.results_repo_id = None
            self.checkpoints_repo_id = None
            return

        self.enabled = True
        print(f"🔐 Authenticated to Hugging Face as: {self.username}")
        print(f"📦 HF Results Dataset Repo: https://huggingface.co/datasets/{self.results_repo_id}")
        if self.checkpoints_repo_id:
            print(f"🧠 HF Checkpoints Model Repo: https://huggingface.co/{self.checkpoints_repo_id}")

    def _qualify_repo(self, name: str) -> str:
        clean = name.strip("/")
        return clean if "/" in clean else f"{self.username}/{clean}"

    def _prefixed(self, rel_path: str) -> str:
        clean_rel = rel_path.lstrip("/")
        return f"{self.run_prefix}/{clean_rel}" if self.run_prefix else clean_rel

    def remote_file_exists(self, rel_path: str, repo_type: str = "dataset") -> bool:
        """Check whether a file already exists in the target HF repository."""
        if not self.enabled or self.api is None:
            return False
        repo_id = self.results_repo_id if repo_type == "dataset" else self.checkpoints_repo_id
        if not repo_id:
            return False
        path_in_repo = self._prefixed(rel_path)
        try:
            return bool(
                self.api.file_exists(
                    repo_id=repo_id,
                    filename=path_in_repo,
                    repo_type=repo_type,
                )
            )
        except Exception:
            try:
                files = self.api.list_repo_files(repo_id=repo_id, repo_type=repo_type)
                return path_in_repo in files
            except Exception:
                return False

    def file_exists_remote(self, rel_path: str, repo_type: str = "dataset") -> bool:
        """Alias for remote_file_exists."""
        return self.remote_file_exists(rel_path, repo_type=repo_type)

    def download_result_if_exists(self, rel_path: str, local_dest_dir: str) -> Optional[str]:
        """Download an existing artifact from the HF dataset repo for resume aggregation."""
        if not self.remote_file_exists(rel_path, repo_type="dataset") or self.api is None:
            return None
        path_in_repo = self._prefixed(rel_path)
        os.makedirs(local_dest_dir, exist_ok=True)
        try:
            return hf_hub_download(
                repo_id=self.results_repo_id,
                filename=path_in_repo,
                repo_type="dataset",
                local_dir=local_dest_dir,
                token=self.token,
            )
        except Exception as exc:
            print(f"⚠️ Failed to download {path_in_repo} from HF for resume: {exc}")
            return None

    def download_remote_file(self, rel_path: str, local_dest_dir: str) -> Optional[str]:
        """Alias for download_result_if_exists."""
        return self.download_result_if_exists(rel_path, local_dest_dir)

    def _retry(self, fn, description: str) -> bool:
        for attempt in range(3):
            try:
                fn()
                return True
            except Exception as exc:
                if attempt == 2:
                    print(f"⚠️ HF upload failed for {description} after 3 attempts: {exc}")
                    return False
                time.sleep(2 ** attempt)
        return False

    def upload_result(self, local_path: str, rel_path: str, commit_message: Optional[str] = None) -> bool:
        """Upload a CSV, PNG, Parquet, or JSON artifact to the HF Dataset repo."""
        if not self.enabled or self.api is None or not self.results_repo_id:
            return False
        path_in_repo = self._prefixed(rel_path)
        msg = commit_message or f"Upload {path_in_repo}"
        return self._retry(
            lambda: self.api.upload_file(
                path_or_fileobj=local_path,
                path_in_repo=path_in_repo,
                repo_id=self.results_repo_id,
                repo_type="dataset",
                commit_message=msg,
            ),
            path_in_repo,
        )

    def upload_results_batch(
        self, items: List[Tuple[str, str]], commit_message: str
    ) -> bool:
        """Upload multiple result files to the HF Dataset repo in one clean commit."""
        if not self.enabled or self.api is None or not self.results_repo_id:
            return False
        ops = [
            CommitOperationAdd(
                path_in_repo=self._prefixed(rel),
                path_or_fileobj=local,
            )
            for local, rel in items
            if os.path.exists(local)
        ]
        if not ops:
            return False
        return self._retry(
            lambda: self.api.create_commit(
                repo_id=self.results_repo_id,
                repo_type="dataset",
                operations=ops,
                commit_message=commit_message,
            ),
            commit_message,
        )

    def upload_checkpoint_dir(
        self, local_dir: str, rel_path: str, commit_message: Optional[str] = None
    ) -> bool:
        """Upload a model checkpoint folder to the HF Model repo."""
        if not self.enabled or self.api is None or not self.checkpoints_repo_id:
            return False
        path_in_repo = self._prefixed(rel_path)
        msg = commit_message or f"Upload checkpoint {path_in_repo}"
        return self._retry(
            lambda: self.api.upload_folder(
                folder_path=local_dir,
                path_in_repo=path_in_repo,
                repo_id=self.checkpoints_repo_id,
                repo_type="model",
                commit_message=msg,
            ),
            path_in_repo,
        )

    def write_and_upload_metadata(
        self,
        local_dir: str,
        args_dict: Dict[str, Any],
        extra_info: Optional[Dict[str, Any]] = None,
        upload: bool = True,
    ) -> str:
        """Persist reproducibility metadata (never includes secrets) and optionally push to HF."""
        git_info = get_git_info()
        sanitized_args = {
            k: v for k, v in args_dict.items() if "token" not in k.lower() and "secret" not in k.lower()
        }
        device = "cpu"
        gpu_name = None
        torch_ver = None
        transformers_ver = None
        try:
            import torch

            torch_ver = torch.__version__
            if torch.cuda.is_available():
                device = "cuda"
                gpu_name = torch.cuda.get_device_name(0)
        except ImportError:
            pass
        try:
            import transformers

            transformers_ver = transformers.__version__
        except ImportError:
            pass

        metadata = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            **git_info,
            "run_prefix": self.run_prefix,
            "device": device,
            "gpu_name": gpu_name,
            "torch_version": torch_ver,
            "transformers_version": transformers_ver,
            "args": sanitized_args,
            "extra_info": extra_info or {},
        }
        meta_path = os.path.join(local_dir, "metadata.json")
        os.makedirs(local_dir, exist_ok=True)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        if upload:
            self.upload_result(meta_path, "metadata.json", "Upload metadata.json")
        return meta_path


def ensure_tawos_snapshots(
    projects: Sequence[str],
    local_dir: str,
    results_repo: str = DEFAULT_RESULTS_REPO_NAME,
    remote_subdir: str = DEFAULT_SNAPSHOTS_SUBDIR,
    extra_search_dirs: Sequence[str] = (),
    token: Optional[str] = None,
    allow_hf_download: bool = True,
) -> Dict[str, str]:
    """Ensure `<PROJECT>_snapshot.parquet` files exist locally, falling back to HF download."""
    os.makedirs(local_dir, exist_ok=True)
    resolved_token = resolve_hf_token(token)

    candidate_repos: List[str] = []
    clean_repo = results_repo.strip("/")
    if "/" in clean_repo:
        candidate_repos.append(clean_repo)
    else:
        if resolved_token:
            try:
                username = HfApi(token=resolved_token).whoami()["name"]
                candidate_repos.append(f"{username}/{clean_repo}")
            except Exception:
                pass
        if f"Snowflake06/{clean_repo}" not in candidate_repos:
            candidate_repos.append(f"Snowflake06/{clean_repo}")

    search_dirs = list(extra_search_dirs) + [
        local_dir,
        os.path.join(local_dir, os.path.normpath(remote_subdir.strip("/"))),
    ]

    found_paths: Dict[str, str] = {}
    clean_subdir = remote_subdir.strip("/")

    for proj in projects:
        p = proj.strip().upper()
        local_path = discover_snapshot_file(p, search_dirs=search_dirs)
        if local_path:
            found_paths[p] = local_path
            continue

        if allow_hf_download:
            remote_file = f"{clean_subdir}/{p}_snapshot.parquet" if clean_subdir else f"{p}_snapshot.parquet"
            for repo_id in candidate_repos:
                try:
                    dl_path = hf_hub_download(
                        repo_id=repo_id,
                        filename=remote_file,
                        repo_type="dataset",
                        local_dir=local_dir,
                        token=resolved_token,
                    )
                    if dl_path and os.path.exists(dl_path):
                        found_paths[p] = dl_path
                        print(f"  ✓ Downloaded {p}_snapshot.parquet from {repo_id}")
                        break
                except Exception:
                    continue

        if p not in found_paths:
            raise FileNotFoundError(
                f"Snapshot parquet missing for '{p}' ({p}_snapshot.parquet). "
                f"Searched local dirs ({search_dirs}) and HF repos ({candidate_repos}). "
                "Please run `python kaggle_TAWOS/prepare_tawos_dataset.py` first or pass `--data-dir`."
            )

    return found_paths
