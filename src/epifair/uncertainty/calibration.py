from __future__ import annotations
import numpy as np

def expected_calibration_error(confidence,correct,n_bins: int=15)->float:
    c=np.asarray(confidence,float); y=np.asarray(correct,float)
    if len(c)==0: return float("nan")
    edges=np.linspace(0,1,n_bins+1); ece=0.0
    for lo,hi in zip(edges[:-1],edges[1:]):
        mask=(c>=lo)&((c<hi) if hi<1 else (c<=hi))
        if mask.any(): ece += mask.mean()*abs(c[mask].mean()-y[mask].mean())
    return float(ece)
def brier_score(confidence,correct)->float:
    c=np.asarray(confidence,float); y=np.asarray(correct,float)
    return float(np.mean((c-y)**2)) if len(c) else float("nan")
def confidence_from_mean_logprob(mean_logprob: float|None)->float|None:
    return None if mean_logprob is None else float(np.clip(np.exp(mean_logprob),0,1))
