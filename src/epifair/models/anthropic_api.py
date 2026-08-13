from __future__ import annotations
from epifair.models.base import ModelAdapter, ModelResponse

class AnthropicAdapter(ModelAdapter):
    provider="anthropic"
    def __init__(self,model_id: str):
        import anthropic
        self.model_id=model_id; self.revision=None; self.client=anthropic.Anthropic()
    def generate(self,prompt: str,*,temperature: float,top_p: float,max_new_tokens: int,seed: int|None=None)->ModelResponse:
        msg=self.client.messages.create(model=self.model_id,max_tokens=max_new_tokens,temperature=temperature,top_p=top_p,messages=[{"role":"user","content":prompt}])
        text="".join(getattr(x,"text","") for x in msg.content)
        return ModelResponse(text=text,input_tokens=getattr(msg.usage,"input_tokens",None),output_tokens=getattr(msg.usage,"output_tokens",None),finish_reason=getattr(msg,"stop_reason",None),metadata={"response_id":msg.id,"temperature_effective":temperature,"top_p_effective":top_p,"seed_requested":seed})
