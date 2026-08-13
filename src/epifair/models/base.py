from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ModelResponse:
    text: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    mean_token_logprob: float | None = None
    sequence_logprob: float | None = None
    finish_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

class ModelAdapter(ABC):
    model_id: str
    provider: str
    revision: str | None = None

    @abstractmethod
    def generate(self, prompt: str, *, temperature: float, top_p: float, max_new_tokens: int, seed: int | None = None) -> ModelResponse:
        raise NotImplementedError
