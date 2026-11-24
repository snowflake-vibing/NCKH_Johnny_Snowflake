"""GPT2SP Core Model Architecture ported cleanly from SR-G3_planning-time-sp."""

from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING, Any
import torch
import torch.nn as nn

if TYPE_CHECKING:
    from transformers import GPT2Config  # pragma: no cover


class GPT2SP(nn.Module):
    """GPT-2 small Story Point regression model with a 3-layer linear head (bias=False)."""

    def __init__(
        self,
        pretrained_model_name: str = "gpt2",
        config: Any = None,
        pad_token_id: int = 50256,
    ) -> None:
        super().__init__()
        from transformers import GPT2Model  # lazy import so CLI --help works without transformers

        if config is not None:
            self.config = config
            self.transformer = GPT2Model(config)
        else:
            self.transformer = GPT2Model.from_pretrained(pretrained_model_name)
            self.config = self.transformer.config

        self.pad_token_id = pad_token_id
        if hasattr(self.config, "pad_token_id") and self.config.pad_token_id is not None:
            self.pad_token_id = self.config.pad_token_id
        else:
            self.config.pad_token_id = self.pad_token_id

        hidden_size = self.config.n_embd  # 768 for gpt2 small

        # 3-layer linear head without bias as specified in Fu & Tantithamthavorn (TSE 2023)
        self.dense1 = nn.Linear(hidden_size, 4 * hidden_size, bias=False)
        self.dense2 = nn.Linear(4 * hidden_size, hidden_size, bias=False)
        self.score = nn.Linear(hidden_size, 1, bias=False)

        self.loss_fct = nn.L1Loss()

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor | None = None,
        labels: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        """Forward pass returning (pooled_logits, l1_loss)."""
        batch_size = input_ids.shape[0]

        transformer_outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )
        hidden_states = transformer_outputs[0]

        hidden_states = self.dense1(hidden_states)
        hidden_states = self.dense2(hidden_states)
        logits = self.score(hidden_states)

        if self.pad_token_id is not None:
            sequence_lengths = torch.ne(input_ids, self.pad_token_id).sum(-1) - 1
            sequence_lengths = torch.clamp(sequence_lengths, min=0)
        else:
            sequence_lengths = torch.full(
                (batch_size,),
                input_ids.shape[1] - 1,
                dtype=torch.long,
                device=input_ids.device,
            )

        batch_indices = torch.arange(batch_size, device=input_ids.device)
        pooled_logits = logits[batch_indices, sequence_lengths]

        loss = None
        if labels is not None:
            target = labels.to(pooled_logits.dtype).view(-1)
            loss = self.loss_fct(pooled_logits.view(-1), target)

        return pooled_logits, loss


def clear_hf_cache(cache_dir: str | None = None) -> None:
    """Remove local Hugging Face download cache between runs to conserve Kaggle disk."""
    target = cache_dir or os.path.expanduser("~/.cache/huggingface/hub")
    if os.path.exists(target):
        shutil.rmtree(target, ignore_errors=True)
