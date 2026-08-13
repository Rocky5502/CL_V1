from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import time, uuid
from epifair.schema import PromptRecord, GenerationRecord
from epifair.utils.hashing import sha256_text, stable_id
from epifair.utils.io import append_jsonl

def run_prompts(adapter,prompts: list[PromptRecord],*,tier: str,out_path: str|Path,samples: int,temperature: float,top_p: float,max_new_tokens: int,base_seed: int=5502,run_id: str|None=None):
    run_id=run_id or f"{tier.lower()}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    for p in prompts:
        for sample_idx in range(samples):
            seed=base_seed+sample_idx; t0=time.perf_counter()
            r=adapter.generate(p.prompt,temperature=temperature,top_p=top_p,max_new_tokens=max_new_tokens,seed=seed)
            latency=(time.perf_counter()-t0)*1000
            record_id=stable_id("g",{"run":run_id,"prompt":p.prompt_id,"model":adapter.model_id,"sample":sample_idx})
            rec=GenerationRecord(run_id=run_id,record_id=record_id,prompt_id=p.prompt_id,scenario_family_id=p.scenario_family_id,model_id=adapter.model_id,provider=adapter.provider,model_revision=getattr(adapter,"revision",None),tier=tier,sample_index=sample_idx,seed=seed,temperature=temperature,top_p=top_p,prompt_sha256=sha256_text(p.prompt),response_text=r.text,response_sha256=sha256_text(r.text),created_at_utc=datetime.now(timezone.utc).isoformat(),latency_ms=latency,input_tokens=r.input_tokens,output_tokens=r.output_tokens,mean_token_logprob=r.mean_token_logprob,sequence_logprob=r.sequence_logprob,finish_reason=r.finish_reason,raw_metadata=r.metadata)
            append_jsonl(out_path,[rec.model_dump(mode="json")])
    return run_id
