# Dataset backup policy

`python scripts/backup_datasets.py --name all` creates local immutable working snapshots and JSON manifests.

For each dataset, the manifest records source metadata, retrieval time, file count, byte count, and SHA-256 for every file. Git-backed datasets additionally record the commit revision. Hugging Face snapshots are resolved through `huggingface_hub`; model/dataset revisions should be frozen again at preregistration.

Do **not** `git add data/raw`. Dataset licenses differ and XNLI/Belebele-scale assets are unsuitable for ordinary Git history.

Recommended backup strategy:

1. primary local SSD snapshot (`data/raw`);
2. second encrypted external drive or institutional storage copy;
3. commit `data/manifests/*.json` after the snapshot is frozen;
4. never modify a frozen snapshot in place — create a new dated snapshot/manifest.
