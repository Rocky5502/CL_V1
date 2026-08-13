from __future__ import annotations
import math
from collections import Counter

def entropy_from_cluster_labels(labels: list[int])->float|None:
    if not labels: return None
    n=len(labels); counts=Counter(labels)
    return -sum((c/n)*math.log(c/n) for c in counts.values())

def cluster_responses(texts: list[str],model_name: str,threshold: float=0.78)->list[int]:
    if not texts: return []
    from sentence_transformers import SentenceTransformer
    import numpy as np
    m=SentenceTransformer(model_name); emb=m.encode(texts,normalize_embeddings=True); labels=[]; centroids=[]
    for v in emb:
        if not centroids: centroids=[v.copy()]; labels.append(0); continue
        sims=np.dot(np.stack(centroids),v); idx=int(np.argmax(sims))
        if float(sims[idx])>=threshold:
            labels.append(idx); centroids[idx]=(centroids[idx]+v)/2; centroids[idx]=centroids[idx]/np.linalg.norm(centroids[idx])
        else: centroids.append(v.copy()); labels.append(len(centroids)-1)
    return labels
