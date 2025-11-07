# Installing mlops dependencies with conda (Windows)

This document shows the recommended steps to create a conda environment and
install the binary-heavy packages (pyarrow, onnxruntime, pytorch) from
`conda-forge` and `pytorch` channels. Using conda avoids trying to build
these packages from source when using a newer Python version.

Quick steps (one-liner):

1. If you don't have conda installed, the helper script will now automatically download
	and silently install Miniconda into your user profile (e.g. `%USERPROFILE%\Miniconda3`) and
	initialize PowerShell for conda use.

2. From the repository root, run the helper PowerShell script (recommended):

```powershell
# from repo root
.\mlops\install_conda.ps1
```

What the script does:
- Creates a conda env `akulearn-mlops` (Python 3.12 by default)
- Installs `pyarrow` and `onnxruntime` from `conda-forge`
- Installs `pytorch` (CPU-only) from `pytorch` channel
- Upgrades pip inside the environment and pip-installs the remaining `mlops/requirements.txt` packages with `--no-deps`

Notes / troubleshooting
- If you prefer a different Python version, run the script with `-PythonVersion 3.11`.
- If `conda` is not on your PATH, open a new Anaconda Prompt or add conda to PATH.
- If `pytorch` install via conda fails, you can follow instructions here for specific CUDA/CPU builds: https://pytorch.org/get-started/locally/
- After install, activate the env:

```powershell
conda activate akulearn-mlops
python -m pip show pyarrow onnxruntime torch
```

- To run the example FastAPI server (inside the activated env):

```powershell
python -m mlops.examples.fastapi_server
```

If you want me to also create a small `install_conda.ps1` that downloads Miniconda automatically, say so and I'll add that — currently the script assumes `conda` is already present.
