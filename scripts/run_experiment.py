from __future__ import annotations
import argparse
from pathlib import Path
from epifair.config import load_yaml
from epifair.models.factory import make_adapter
from epifair.schema import PromptRecord
from epifair.utils.io import read_jsonl
from epifair.runners.core import run_prompts

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--tier",choices=["A","B"],required=True); ap.add_argument("--config",default="configs/experiment.yaml"); ap.add_argument("--model"); ap.add_argument("--limit",type=int); a=ap.parse_args()
    exp=load_yaml(a.config); mcfg=load_yaml("configs/frozen_models.yaml" if Path("configs/frozen_models.yaml").exists() else "configs/models.yaml")
    models=mcfg["models"]
    if a.model: models=[m for m in models if m["id"]==a.model]
    else: models=[m for m in models if m.get("enabled")]
    pfile=Path("data/benchmark/main_prompts.jsonl")
    if not pfile.exists(): raise SystemExit("Main benchmark not frozen. Build/validate translations and write data/benchmark/main_prompts.jsonl first.")
    prompts=[PromptRecord.model_validate(x) for x in read_jsonl(pfile)]
    if a.limit: prompts=prompts[:a.limit]
    tc=exp["tier_a" if a.tier=="A" else "tier_b"]
    for spec in models:
        adapter=make_adapter(spec); samples=1 if a.tier=="A" else (tc["open_samples_per_prompt"] if spec["group"]=="open" else tc["api_samples_per_prompt"])
        out=f"outputs/tier_{a.tier.lower()}/{spec['id']}.jsonl"
        run_prompts(adapter,prompts,tier=a.tier,out_path=out,samples=samples,temperature=tc["temperature"],top_p=tc["top_p"],max_new_tokens=tc["max_new_tokens"],base_seed=exp["seed"])
if __name__=="__main__": main()
