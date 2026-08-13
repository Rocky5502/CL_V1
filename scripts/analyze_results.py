from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from epifair.labeling.actions import classify_action
from epifair.uncertainty.calibration import confidence_from_mean_logprob

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--config",default="configs/experiment.yaml"); a=ap.parse_args()
    files=list(Path("outputs").glob("tier_*/*.jsonl"))
    if not files: raise SystemExit("No experiment outputs found.")
    frames=[pd.read_json(p,lines=True) for p in files]; df=pd.concat(frames,ignore_index=True)
    labels=df.response_text.map(classify_action); df["action"]=[x[0].value for x in labels]; df["action_classifier_confidence"]=[x[1] for x in labels]
    df["logprob_confidence"]=df.mean_token_logprob.map(confidence_from_mean_logprob)
    Path("results/derived").mkdir(parents=True,exist_ok=True); df.to_parquet("results/derived/generations_labeled.parquet",index=False)
    print("Wrote results/derived/generations_labeled.parquet")
    print("STOP: correctness, unsupported-assumption, and main statistical tables require benchmark-grounded labels and validated action classifier.")
if __name__=="__main__": main()
