"""Hugging Face Hub integration for Secrets auth, auto-resume, checkpoints, and results."""

from datetime import datetime, timezone
import json
import os
import subprocess
import time
from typing import Any, Dict, List, Optional, Tuple
from huggingface_hub import CommitOperationAdd, HfApi, hf_hub_download


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
        """Upload a CSV, PNG, or JSON artifact to the HF Dataset repo."""
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
        h5py_ver = None
        try:
            import torch

            torch_ver = torch.__version__
            if torch.cuda.is_available():
                device = "cuda"
                gpu_name = torch.cuda.get_device_name(0)
        except ImportError:
            pass
        try:
            import h5py

            h5py_ver = h5py.__version__
        except ImportError:
            pass

        metadata = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            **git_info,
            "run_prefix": self.run_prefix,
            "device": device,
            "gpu_name": gpu_name,
            "torch_version": torch_ver,
            "h5py_version": h5py_ver,
            "args": sanitized_args,
            "extra_info": extra_info or {},
        }
        meta_path = os.path.join(local_dir, "metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        if upload:
            self.upload_result(meta_path, "metadata.json", "Upload metadata.json")
        return meta_path
