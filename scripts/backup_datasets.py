from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from epifair.config import load_yaml
from epifair.utils.hashing import sha256_file


def hash_tree(root: Path) -> list[dict]:
    rows = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and ".git" not in p.parts:
            rows.append({"path": str(p.relative_to(root)), "bytes": p.stat().st_size, "sha256": sha256_file(p)})
    return rows


def snapshot_hf(name: str, spec: dict, raw_root: Path):
    from huggingface_hub import HfApi, snapshot_download
    info = HfApi().dataset_info(spec["repo_id"], revision=spec.get("revision"))
    resolved_revision = info.sha
    dest = raw_root / name
    path = snapshot_download(repo_id=spec["repo_id"], repo_type=spec.get("repo_type", "dataset"), revision=resolved_revision, local_dir=dest, allow_patterns=spec.get("snapshot_allow_patterns"))
    return Path(path), {"resolved_via": "huggingface_hub", "resolved_revision": resolved_revision, "last_modified": str(getattr(info, "last_modified", None))}


def snapshot_git(name: str, spec: dict, raw_root: Path):
    dest = raw_root / name
    if dest.exists(): shutil.rmtree(dest)
    subprocess.run(["git", "clone", "--depth", "1", spec["url"], str(dest)], check=True)
    rev = subprocess.check_output(["git", "-C", str(dest), "rev-parse", "HEAD"], text=True).strip()
    return dest, {"resolved_via": "git", "git_revision": rev}


def write_manifest(name: str, spec: dict, path: Path, meta: dict, manifests: Path) -> dict:
    files = hash_tree(path)
    manifest = {"schema_version": 1, "dataset": name, "snapshot_time_utc": datetime.now(timezone.utc).isoformat(), "spec": spec, "meta": meta, "file_count": len(files), "total_bytes": sum(x["bytes"] for x in files), "files": files}
    target = manifests / f"{name}.json"
    target.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    manifest["manifest_sha256"] = sha256_file(target)
    return manifest


def verify_snapshot(name: str, raw_root: Path, manifests: Path) -> bool:
    manifest_path = manifests / f"{name}.json"; data_root = raw_root / name
    if not manifest_path.exists() or not data_root.exists():
        print(f"{name}: MISSING snapshot or manifest"); return False
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = {x["path"]: x for x in manifest["files"]}; actual = {x["path"]: x for x in hash_tree(data_root)}
    ok = expected.keys() == actual.keys()
    if ok: ok = all(expected[k]["sha256"] == actual[k]["sha256"] for k in expected)
    print(f"{name}: {'OK' if ok else 'MISMATCH'} ({len(actual)} files)"); return ok


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--name", default="all"); ap.add_argument("--list", action="store_true"); ap.add_argument("--verify", action="store_true"); a=ap.parse_args()
    reg=load_yaml("configs/datasets.yaml")["datasets"]
    if a.list:
        for n,spec in reg.items(): print(f"{n:16s} {spec['source_type']:12s} {spec.get('repo_id', spec.get('url'))}")
        return
    names=list(reg) if a.name == "all" else [a.name]
    unknown=[n for n in names if n not in reg]
    if unknown: raise SystemExit(f"Unknown datasets: {unknown}")
    raw=Path("data/raw"); manifests=Path("data/manifests"); raw.mkdir(parents=True,exist_ok=True); manifests.mkdir(parents=True,exist_ok=True)
    if a.verify:
        good=all(verify_snapshot(name,raw,manifests) for name in names); raise SystemExit(0 if good else 2)
    for name in names:
        spec=reg[name]
        if spec["source_type"] == "huggingface": path,meta=snapshot_hf(name,spec,raw)
        elif spec["source_type"] == "git": path,meta=snapshot_git(name,spec,raw)
        else: raise ValueError(spec["source_type"])
        manifest=write_manifest(name,spec,path,meta,manifests)
        print(name,manifest["file_count"],manifest["total_bytes"],meta.get("resolved_revision",meta.get("git_revision")))

if __name__ == "__main__": main()
