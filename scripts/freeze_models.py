from __future__ import annotations
import json, os
from pathlib import Path
from datetime import datetime, timezone
from epifair.config import load_yaml

def main():
    cfg=load_yaml("configs/models.yaml"); frozen=[]
    from huggingface_hub import HfApi
    api=HfApi()
    for spec in cfg["models"]:
        s=dict(spec)
        if spec["provider"]=="hf":
            info=api.model_info(spec["model_id"],revision=spec.get("revision")); s["revision"]=info.sha; s["last_modified"]=str(info.last_modified)
        elif spec.get("model_id_env"):
            s["model_id"]=os.getenv(spec["model_id_env"])
            if s["enabled"] and not s["model_id"]: raise RuntimeError(f"Missing {spec['model_id_env']}")
        frozen.append(s)
    out={"frozen_at_utc":datetime.now(timezone.utc).isoformat(),"models":frozen}
    Path("configs/frozen_models.yaml").write_text(__import__('yaml').safe_dump(out,sort_keys=False),encoding="utf-8")
    Path("artifacts/model_freeze.json").parent.mkdir(parents=True,exist_ok=True)
    Path("artifacts/model_freeze.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print("Wrote configs/frozen_models.yaml")
if __name__=="__main__": main()
