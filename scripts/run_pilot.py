from __future__ import annotations
import argparse
from epifair.models.mock import MockAdapter
from epifair.schema import PromptRecord
from epifair.utils.io import read_jsonl
from epifair.runners.core import run_prompts

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--model",default="mock"); ap.add_argument("--limit",type=int,default=24); a=ap.parse_args()
    if a.model!="mock": raise SystemExit("Pilot CLI currently enables mock only; use run_experiment.py for configured models.")
    prompts=[PromptRecord.model_validate(x) for x in read_jsonl("data/benchmark/pilot_prompts_en.jsonl")][:a.limit]
    rid=run_prompts(MockAdapter(),prompts,tier="pilot",out_path="outputs/pilot/mock.jsonl",samples=1,temperature=0,top_p=1,max_new_tokens=128); print(rid)
if __name__=="__main__": main()
