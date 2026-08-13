# Reproducibility checklist

- [ ] Exact CPU model and core/thread count captured
- [ ] GPU name, usable memory, driver, and `nvidia-smi -q` archived
- [ ] Windows build and WSL kernel recorded
- [ ] Python, PyTorch, CUDA runtime, Transformers, and package freeze archived
- [ ] Dataset revisions and SHA-256 manifests frozen
- [ ] Reviewed confirmatory benchmark frozen and hash-recorded
- [ ] Translation validation complete
- [ ] Exact local checkpoint SHAs and hosted model IDs frozen
- [ ] System/user prompts and generation settings frozen
- [ ] Random-seed and retry policy frozen
- [ ] Action-labeling validation clears preregistered thresholds
- [ ] Statistical analysis plan signed off before confirmatory analysis
- [ ] Raw outputs remain append-only and hashed
- [ ] Null results and failed runs are retained
- [ ] Paper tables and figures are generated from code
