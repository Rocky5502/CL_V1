from __future__ import annotations
from pathlib import Path
import json
from typing import Iterable, Any

def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    out=[]
    with Path(path).open("r", encoding="utf-8") as f:
        for i,line in enumerate(f,1):
            if not line.strip(): continue
            try: out.append(json.loads(line))
            except json.JSONDecodeError as e: raise ValueError(f"Bad JSONL {path}:{i}: {e}") from e
    return out

def append_jsonl(path: str | Path, rows: Iterable[dict[str, Any]]) -> None:
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a",encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True)+"\n")

def write_jsonl(path: str | Path, rows: Iterable[dict[str, Any]]) -> None:
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w",encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True)+"\n")
