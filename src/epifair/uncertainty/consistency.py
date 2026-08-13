from __future__ import annotations
from collections import Counter

def normalized_mode_consistency(labels: list[str])->float|None:
    return None if not labels else max(Counter(labels).values())/len(labels)
