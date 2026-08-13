from __future__ import annotations
import argparse, json, platform, shutil, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

def cmd(args):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=30,check=False); return {"cmd":args,"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
    except Exception as e: return {"cmd":args,"error":repr(e)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--write",default="artifacts/preflight"); a=ap.parse_args()
    out=Path(a.write); out.mkdir(parents=True,exist_ok=True)
    report={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"platform":platform.platform(),"python":sys.version,"cpu":platform.processor(),"machine":platform.machine(),"disk":shutil.disk_usage("."),"commands":[]}
    for c in [["nvidia-smi","--query-gpu=name,memory.total,driver_version","--format=csv"],["nvidia-smi","-q"],["uname","-a"],["wsl.exe","--version"]]: report["commands"].append(cmd(c))
    try:
        import torch
        report["torch"]={"version":torch.__version__,"cuda_available":torch.cuda.is_available(),"cuda_version":torch.version.cuda,"device_count":torch.cuda.device_count(),"devices":[torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]}
    except Exception as e: report["torch"]={"error":repr(e)}
    (out/"preflight.json").write_text(json.dumps(report,indent=2,default=str),encoding="utf-8"); print(json.dumps(report,indent=2,default=str))
if __name__=="__main__": main()
