from __future__ import annotations
from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, Field

class InformationState(str, Enum):
    UNDERSPECIFIED = "underspecified"
    SUFFICIENT = "sufficient"
    MISLEADING = "misleading"

class EpistemicAction(str, Enum):
    ANSWER = "answer"
    CLARIFY = "clarify"
    CHECK = "check"
    ABSTAIN = "abstain"
    REFUSE = "refuse"
    ASSUME = "assume"
    UNKNOWN = "unknown"

class PromptRecord(BaseModel):
    prompt_id: str
    scenario_family_id: str
    domain: str
    language: str
    information_state: InformationState
    social_dimension: str
    cue_label: str
    cue_variant: Literal["A", "B"]
    paraphrase_id: int = 0
    prompt: str
    normatively_relevant_facts: dict[str, Any] = Field(default_factory=dict)
    cue_should_be_irrelevant: bool = True
    expected_action: list[EpistemicAction] = Field(default_factory=list)
    source: str = "epifair_constructed"
    translation_status: str = "source_language"

class GenerationRecord(BaseModel):
    run_id: str
    record_id: str
    prompt_id: str
    scenario_family_id: str
    model_id: str
    provider: str
    model_revision: str | None = None
    tier: Literal["A", "B", "pilot"]
    sample_index: int
    seed: int | None = None
    temperature: float
    top_p: float
    prompt_sha256: str
    response_text: str
    response_sha256: str
    created_at_utc: str
    latency_ms: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    mean_token_logprob: float | None = None
    sequence_logprob: float | None = None
    finish_reason: str | None = None
    raw_metadata: dict[str, Any] = Field(default_factory=dict)

class ActionScore(BaseModel):
    record_id: str
    action: EpistemicAction
    confidence: float = Field(ge=0, le=1)
    method: str
    rationale_code: str | None = None

class CorrectnessScore(BaseModel):
    record_id: str
    correct: bool | None
    score: float | None = Field(default=None, ge=0, le=1)
    method: str
    judge_model_id: str | None = None
    notes: str | None = None
