from __future__ import annotations
from epifair.models.base import ModelAdapter, ModelResponse

class OpenAIAdapter(ModelAdapter):
    provider="openai"
    def __init__(self,model_id: str):
        from openai import OpenAI
        self.model_id=model_id; self.revision=None; self.client=OpenAI()
    def generate(self,prompt: str,*,temperature: float,top_p: float,max_new_tokens: int,seed: int|None=None)->ModelResponse:
        response=self.client.responses.create(model=self.model_id,input=prompt,max_output_tokens=max_new_tokens)
        usage=getattr(response,"usage",None)
        return ModelResponse(text=response.output_text,input_tokens=getattr(usage,"input_tokens",None),output_tokens=getattr(usage,"output_tokens",None),metadata={"response_id":response.id,"temperature_requested":temperature,"top_p_requested":top_p,"seed_requested":seed,"sampling_controls_sent":[]})
