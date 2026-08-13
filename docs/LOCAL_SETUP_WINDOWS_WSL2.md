# Windows 10 Pro + WSL2 setup

Before model selection, verify the reported GPU-memory configuration rather than assuming it is physical VRAM.

Windows PowerShell commands to archive:

```powershell
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber
```

Install/update WSL2 and Ubuntu 24.04, clone the repository, and run `bash scripts/setup_wsl.sh` inside Ubuntu. The Windows NVIDIA driver provides GPU support to WSL; do not install a second Linux display driver inside WSL.

Keep model/data caches on the Samsung 990 PRO and retain substantial free space for temporary model files and raw generations. Store secrets only in `.env`, which is Git-ignored.
