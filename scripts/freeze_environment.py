from pathlib import Path
import json, subprocess, sys
from datetime import datetime, timezone
out=Path("artifacts/environment"); out.mkdir(parents=True,exist_ok=True)
(out/"pip-freeze.txt").write_text(subprocess.check_output([sys.executable,"-m","pip","freeze"],text=True),encoding="utf-8")
meta={"frozen_at_utc":datetime.now(timezone.utc).isoformat(),"python":sys.version}
(out/"environment.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
print(out)
