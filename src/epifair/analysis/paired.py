from __future__ import annotations
import pandas as pd

def within_family_contrast(df: pd.DataFrame, outcome: str) -> pd.DataFrame:
    keys=["scenario_family_id","information_state","language","paraphrase_id","model_id"]
    piv=df.pivot_table(index=keys,columns="cue_variant",values=outcome,aggfunc="mean")
    piv=piv.dropna(subset=["A","B"]).reset_index(); piv["contrast_A_minus_B"]=piv["A"]-piv["B"]
    return piv
