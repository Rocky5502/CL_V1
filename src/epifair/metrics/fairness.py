from __future__ import annotations
import numpy as np

def absolute_gap(a,b)->float: return float(abs(float(a)-float(b)))
def rate(values)->float:
    vals=np.asarray(list(values),dtype=float); return float(vals.mean()) if len(vals) else float("nan")
def paired_gap(rows,outcome: str,pair_key: str="cue_variant")->float:
    a=[r[outcome] for r in rows if r[pair_key]=="A"]; b=[r[outcome] for r in rows if r[pair_key]=="B"]
    return absolute_gap(rate(a),rate(b))
def wrong_overconfidence_rate(correct,confidence,threshold: float=0.8)->float:
    c=np.asarray(correct,dtype=bool); p=np.asarray(confidence,float)
    return float((~c & (p>=threshold)).mean()) if len(c) else float("nan")
