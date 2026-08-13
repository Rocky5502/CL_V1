from __future__ import annotations
from epifair.models.base import ModelAdapter, ModelResponse

class GeminiAdapter(ModelAdapter):
    provider="gemini"
    def __init__(self,model_id: str):
        from google import genai
        self.model_id=model_id; self.revision=None; self.client=genai.Client()
    def generate(self,prompt: str,*,temperature: float,top_p: float,max_new_tokens: int,seed: int|None=None)->ModelResponse:
        from google.genai import types
        cfg=types.GenerateContentConfig(temperature=temperature,top_p=top_p,max_output_tokens=max_new_tokens)
        r=self.client.models.generate_content(model=self.model_id,contents=prompt,config=cfg)
        usage=getattr(r,"usage_metadata",None)
        return ModelResponse(text=r.text or "",input_tokens=getattr(usage,"prompt_token_count",None),output_tokens=getattr(usage,"candidates_token_count",None),metadata={"temperature_effective":temperature,"top_p_effective":top_p,"seed_requested":seed})
