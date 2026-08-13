from __future__ import annotations

import os

from epifair.models.mock import MockAdapter


def make_adapter(spec: dict):
    provider = spec["provider"]
    if provider == "mock":
        return MockAdapter()

    model_id = spec.get("model_id")
    if spec.get("model_id_env"):
        model_id = os.getenv(spec["model_id_env"])
        if not model_id:
            raise RuntimeError(f"Set {spec['model_id_env']} before using {spec['id']}")

    if provider == "hf":
        from epifair.models.hf_local import HFLocalAdapter

        return HFLocalAdapter(
            model_id,
            revision=spec.get("revision"),
            dtype={"bf16": "bfloat16", "fp16": "float16"}.get(spec.get("precision"), "bfloat16"),
            loader=spec.get("loader", "causal_lm"),
            chat_template_kwargs=spec.get("chat_template_kwargs", {}),
        )
    if provider == "openai":
        from epifair.models.openai_api import OpenAIAdapter

        return OpenAIAdapter(model_id)
    if provider == "anthropic":
        from epifair.models.anthropic_api import AnthropicAdapter

        return AnthropicAdapter(model_id)
    if provider == "gemini":
        from epifair.models.gemini_api import GeminiAdapter

        return GeminiAdapter(model_id)
    raise ValueError(provider)
