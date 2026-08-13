from epifair.models.base import ModelAdapter, ModelResponse

class MockAdapter(ModelAdapter):
    model_id="mock-epifair"
    provider="mock"
    revision="deterministic-v1"
    def generate(self,prompt: str,*,temperature: float,top_p: float,max_new_tokens: int,seed: int|None=None)->ModelResponse:
        low=prompt.lower()
        if "not enough" in low or "missing" in low or "unknown" in low:
            text="I need more information before I can answer reliably. Could you clarify the missing relevant detail?"
        elif "conflicting" in low or "contradict" in low:
            text="The evidence is conflicting, so I would verify the relevant information before answering."
        else:
            text="Based only on the provided relevant information, the supported answer is the stated option."
        return ModelResponse(text=text, input_tokens=len(prompt.split()), output_tokens=len(text.split()))
