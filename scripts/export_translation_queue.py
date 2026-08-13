from pathlib import Path
import csv
from epifair.utils.io import read_jsonl
from epifair.config import load_yaml
rows=read_jsonl("data/benchmark/pilot_prompts_en.jsonl")
langs=load_yaml("configs/languages.yaml")["languages"]
out=Path("data/translation/queue.csv"); out.parent.mkdir(parents=True,exist_ok=True)
with out.open("w",newline="",encoding="utf-8") as f:
    wr=csv.DictWriter(f,fieldnames=["prompt_id","target_language","source_text","translation","translator_id","reviewer_id","status"]); wr.writeheader()
    for r in rows:
        for code in langs:
            if code=="en": continue
            wr.writerow({"prompt_id":r["prompt_id"],"target_language":code,"source_text":r["prompt"],"translation":"","translator_id":"","reviewer_id":"","status":"TBD"})
print(out)
