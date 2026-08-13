from __future__ import annotations
import hashlib, json
from pathlib import Path

IGNORE_PREFIXES=(".git/",".venv/","outputs/","data/raw/","data/cache/")

def main():
    rows=[]
    for p in sorted(Path('.').rglob('*')):
        if not p.is_file(): continue
        rel=p.as_posix().lstrip('./')
        if rel=="MANIFEST.json" or any(rel.startswith(x) for x in IGNORE_PREFIXES) or "__pycache__" in rel or ".pytest_cache" in rel: continue
        b=p.read_bytes(); rows.append({"path":rel,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
    Path("MANIFEST.json").write_text(json.dumps({"schema_version":1,"files":rows},indent=2)+"\n")
    print(f"Wrote MANIFEST.json for {len(rows)} files")
if __name__=="__main__": main()
