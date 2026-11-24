"""Dataset and DataLoader utilities for TAWOS Planning-Time Snapshot experiments."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Sequence
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase  # pragma: no cover

try:
    from kaggle_TAWOS.config import MAX_SP, SPLIT, discover_snapshot_file
except ImportError:
    from config import MAX_SP, SPLIT, discover_snapshot_file  # type: ignore


class StoryPointDataset(Dataset):
    """PyTorch Dataset for story point estimation with optional pre-tokenization."""

    def __init__(
        self,
        texts: Sequence[str],
        labels: Sequence[float] | np.ndarray | None = None,
        tokenizer: Any = None,
        max_length: int = 128,
    ) -> None:
        self.texts = [str(t) if t is not None else "" for t in texts]
        self.max_length = max_length

        if tokenizer is not None:
            if getattr(tokenizer, "pad_token", None) is None:
                tokenizer.pad_token = tokenizer.eos_token
                tokenizer.pad_token_id = tokenizer.eos_token_id

            encodings = tokenizer(
                self.texts,
                truncation=True,
                padding="max_length",
                max_length=max_length,
                return_tensors="pt",
            )
            self.input_ids = encodings["input_ids"]
            self.attention_mask = encodings["attention_mask"]
        else:
            self.input_ids = None
            self.attention_mask = None

        if labels is not None:
            self.labels = torch.tensor(np.asarray(labels, dtype=np.float32), dtype=torch.float32)
        else:
            self.labels = None

    def __len__(self) -> int:
        if self.input_ids is not None:
            return len(self.input_ids)
        return len(self.texts)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        item: dict[str, torch.Tensor] = {}
        if self.input_ids is not None and self.attention_mask is not None:
            item["input_ids"] = self.input_ids[idx]
            item["attention_mask"] = self.attention_mask[idx]
        if self.labels is not None:
            item["label"] = self.labels[idx]
            item["labels"] = self.labels[idx]
        return item


def load_tawos_snapshot(
    project: str,
    parquet_path: Optional[str] = None,
    setting: Optional[str] = None,
    input_mode: str = "title_description",
    max_sp: float = MAX_SP,
    search_dirs: Sequence[str] = (),
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load TAWOS snapshot parquet and partition chronologically by Planning_Date (0.6/0.2/0.2)."""
    if setting is not None and setting not in ("final", "cross", "planning"):
        raise ValueError(f"Unknown setting: {setting}. Must be 'final', 'cross', or 'planning'.")

    resolved_path = parquet_path or discover_snapshot_file(project, search_dirs=search_dirs)
    if not resolved_path:
        raise FileNotFoundError(
            f"Snapshot parquet not found for '{project}'. Pass parquet_path or run prepare_tawos_dataset.py."
        )

    s = pd.read_parquet(resolved_path)
    sp = s[["Story_Point", "Final_Story_Point"]]
    s = s[sp.notna().all(axis=1) & (sp.max(axis=1) <= max_sp)].copy()

    for pre in ("", "Final_"):
        title_col = pre + "Title"
        desc_col = pre + "Description"
        if input_mode == "title_only":
            s[pre + "Text"] = s[title_col].fillna("").astype(str)
        else:
            s[pre + "Text"] = s[title_col].fillna("").astype(str) + " " + s[desc_col].fillna("").astype(str)

    s["changed"] = (
        (s.Story_Point != s.Final_Story_Point)
        | (s.Title.fillna("") != s.Final_Title.fillna(""))
        | (s.Description.fillna("") != s.Final_Description.fillna(""))
    )

    s = s.sort_values(["Planning_Date", "ID"]).reset_index(drop=True)

    a = round(len(s) * SPLIT[0])
    b = round(len(s) * (SPLIT[0] + SPLIT[1]))

    train_df = s.iloc[:a].copy()
    val_df = s.iloc[a:b].copy()
    test_df = s.iloc[b:].copy()

    if setting in ("final", "cross"):
        train_text_col, train_label_col = "Final_Text", "Final_Story_Point"
    else:
        train_text_col, train_label_col = "Text", "Story_Point"

    if setting == "final":
        test_text_col, test_label_col = "Final_Text", "Final_Story_Point"
    else:
        test_text_col, test_label_col = "Text", "Story_Point"

    for df_split in (train_df, val_df):
        df_split["text"] = df_split[train_text_col]
        df_split["label"] = df_split[train_label_col].astype(float)

    test_df["text"] = test_df[test_text_col]
    test_df["label"] = test_df[test_label_col].astype(float)

    return train_df, val_df, test_df


def create_dataloader(
    dataset: Dataset,
    batch_size: int = 32,
    shuffle: bool = False,
    num_workers: int = 0,
) -> DataLoader:
    """Create a standard PyTorch DataLoader."""
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
    )
