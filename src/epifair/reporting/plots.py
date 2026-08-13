from __future__ import annotations
from pathlib import Path

def save_action_by_uncertainty(df,out: str|Path,action_col: str="is_clarify",uncertainty_col: str="uncertainty"):
    import matplotlib.pyplot as plt
    import pandas as pd
    work=df.dropna(subset=[uncertainty_col,action_col]).copy(); work["bin"]=pd.qcut(work[uncertainty_col],q=10,duplicates="drop")
    g=work.groupby(["bin","cue_variant"],observed=True).agg(x=(uncertainty_col,"mean"),y=(action_col,"mean")).reset_index()
    fig,ax=plt.subplots(figsize=(6.2,4.0))
    for cue,sub in g.groupby("cue_variant"): ax.plot(sub.x,sub.y,marker="o",label=f"Condition {cue}")
    ax.set_xlabel("Estimated uncertainty"); ax.set_ylabel("Action probability"); ax.legend(frameon=False)
    fig.tight_layout(); Path(out).parent.mkdir(parents=True,exist_ok=True); fig.savefig(out,dpi=300,bbox_inches="tight"); plt.close(fig)
