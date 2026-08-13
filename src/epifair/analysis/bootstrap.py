from __future__ import annotations
import numpy as np

def clustered_bootstrap_mean(df, value_col: str, cluster_col: str, n_boot: int=2000, seed: int=5502):
    rng=np.random.default_rng(seed); clusters=df[cluster_col].dropna().unique(); vals=[]
    for _ in range(n_boot):
        draw=rng.choice(clusters,size=len(clusters),replace=True); sample=[]
        for c in draw: sample.extend(df.loc[df[cluster_col]==c,value_col].tolist())
        vals.append(float(np.mean(sample)))
    return {"mean":float(df[value_col].mean()),"ci_low":float(np.quantile(vals,.025)),"ci_high":float(np.quantile(vals,.975))}
