from pathlib import Path
import pandas as pd
from epifair.reporting.plots import save_action_by_uncertainty
p=Path("results/derived/generations_labeled.parquet")
if not p.exists(): raise SystemExit("Run analysis first")
df=pd.read_parquet(p)
if "uncertainty" not in df: raise SystemExit("No frozen uncertainty column yet; do not invent it.")
df["is_clarify"]=(df.action=="clarify").astype(int)
save_action_by_uncertainty(df,"paper/generated/fig_action_uncertainty.pdf")
