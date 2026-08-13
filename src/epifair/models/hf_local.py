from __future__ import annotations

from typing import Any
import torch
from epifair.models.base import ModelAdapter, ModelResponse

class HFLocalAdapter(ModelAdapter):
    def __init__(self, model_id: str, revision: str | None = None, dtype: str = "bfloat16", loader: str = "causal_lm", chat_template_kwargs: dict[str, Any] | None = None) -> None:
        from transformers import AutoModelForCausalLM, AutoModelForImageTextToText, AutoProcessor, AutoTokenizer
        self.model_id=model_id; self.provider="hf"; self.revision=revision; self.loader=loader; self.chat_template_kwargs=chat_template_kwargs or {}
        torch_dtype=getattr(torch,dtype)
        common=dict(revision=revision,torch_dtype=torch_dtype,device_map="auto",trust_remote_code=False)
        if loader=="causal_lm":
            self.processor=None
            self.tokenizer=AutoTokenizer.from_pretrained(model_id,revision=revision,trust_remote_code=False)
            self.model=AutoModelForCausalLM.from_pretrained(model_id,**common).eval()
        elif loader=="image_text_to_text":
            self.processor=AutoProcessor.from_pretrained(model_id,revision=revision,trust_remote_code=False)
            self.tokenizer=getattr(self.processor,"tokenizer",None)
            self.model=AutoModelForImageTextToText.from_pretrained(model_id,**common).eval()
        else:
            raise ValueError(f"Unsupported HF loader: {loader}")

    def _prepare(self,prompt: str):
        messages=[{"role":"user","content":[{"type":"text","text":prompt}]}]
        if self.processor is not None:
            rendered=self.processor.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,**self.chat_template_kwargs)
            return self.processor(text=rendered,return_tensors="pt").to(self.model.device)
        text_messages=[{"role":"user","content":prompt}]
        rendered=self.tokenizer.apply_chat_template(text_messages,tokenize=False,add_generation_prompt=True,**self.chat_template_kwargs) if hasattr(self.tokenizer,"apply_chat_template") else prompt
        return self.tokenizer(rendered,return_tensors="pt").to(self.model.device)

    @torch.inference_mode()
    def generate(self,prompt: str,*,temperature: float,top_p: float,max_new_tokens: int,seed: int|None=None)->ModelResponse:
        if seed is not None:
            torch.manual_seed(seed)
            if torch.cuda.is_available(): torch.cuda.manual_seed_all(seed)
        batch=self._prepare(prompt); input_len=batch["input_ids"].shape[1]; do_sample=temperature>0
        kwargs={"max_new_tokens":max_new_tokens,"do_sample":do_sample,"return_dict_in_generate":True,"output_scores":True}
        if do_sample: kwargs.update(temperature=temperature,top_p=top_p)
        out=self.model.generate(**batch,**kwargs); seq=out.sequences[0]; gen=seq[input_len:]
        decoder=self.tokenizer or self.processor; text=decoder.decode(gen,skip_special_tokens=True)
        lps=[]
        for i,score in enumerate(out.scores or []):
            if i>=len(gen): break
            lps.append(torch.log_softmax(score[0].float(),dim=-1)[gen[i]].item())
        return ModelResponse(text=text,input_tokens=input_len,output_tokens=len(gen),mean_token_logprob=sum(lps)/len(lps) if lps else None,sequence_logprob=sum(lps) if lps else None,metadata={"loader":self.loader,"revision":self.revision,"temperature_effective":temperature if do_sample else 0.0,"top_p_effective":top_p if do_sample else None})
