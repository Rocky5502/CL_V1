#!/usr/bin/env bash
set -euo pipefail

# EpiFair WSL2 bootstrap. Run inside Ubuntu 24.04 under WSL2.
# NVIDIA's WSL guidance: install/update the NVIDIA Windows driver on the host;
# do NOT install a Linux display driver inside WSL.

if ! grep -qi microsoft /proc/version; then
  echo "WARNING: This script is designed for WSL2. /proc/version does not look like WSL." >&2
fi

sudo apt-get update
sudo apt-get install -y git git-lfs build-essential python3.11 python3.11-venv python3-pip jq unzip rsync

git lfs install
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel

# Install research/core + data/API/dev stack first. GPU torch is installed explicitly below.
pip install -e '.[data,api,dev]'

# Current Blackwell-capable frozen bootstrap audited 2026-08-13.
# PyTorch 2.12.1 publishes a CUDA 13.0 wheel and recommends CUDA 13.0+ for newer Blackwell GPUs.
pip install torch==2.12.1 --index-url https://download.pytorch.org/whl/cu130
pip install 'transformers>=4.51' 'accelerate>=1.2' 'sentence-transformers>=3.3' 'safetensors>=0.4'

python scripts/preflight.py --write artifacts/preflight
python - <<'PY2'
import torch
print('torch', torch.__version__)
print('torch CUDA runtime', torch.version.cuda)
print('CUDA available', torch.cuda.is_available())
if torch.cuda.is_available():
    print('GPU', torch.cuda.get_device_name(0))
    print('capability', torch.cuda.get_device_capability(0))
PY2

echo "Core environment created. Review artifacts/preflight/preflight.json before downloading models."
echo "If the host NVIDIA driver is too old for CUDA 13.0, update the Windows driver first; do not install a Linux NVIDIA display driver in WSL."
