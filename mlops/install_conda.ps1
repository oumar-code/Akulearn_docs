<#
PowerShell helper to create a conda environment and install binary packages
for the mlops demo. This script expects `conda` (Miniconda/Anaconda) to be
installed and available on PATH. It will:

- create a conda env named `akulearn-mlops` (Python 3.12)
- install heavy binary packages from conda-forge / pytorch channels
- upgrade pip inside the env and pip-install the pip-only requirements

Run this from the repo root (where `mlops\requirements.txt` exists):
    .\mlops\install_conda.ps1

Note: On Windows you may need to run PowerShell as Administrator to allow
activation scripts or adjust your execution policy.
#>

param(
    [string]$EnvName = "akulearn-mlops",
    [string]$PythonVersion = "3.12",
    [switch]$Force
)

function ExitWith($code, $msg) {
    Write-Host $msg
    exit $code
}

Write-Host "== Akulearn: conda installer helper =="

# Check for conda
try {
    $condaVersion = & conda --version 2>$null
} catch {
    ExitWith 1 "conda not found on PATH. Please install Miniconda or Anaconda and re-run. https://docs.conda.io/en/latest/miniconda.html"
}

Write-Host "Found conda: $condaVersion"

if (Get-Command conda -ErrorAction SilentlyContinue) {
    Write-Host "Creating conda environment '$EnvName' with Python $PythonVersion..."
    if ($Force) {
        conda remove -n $EnvName --all -y
    }
    conda create -n $EnvName python=$PythonVersion -y || ExitWith 2 "Failed to create conda env."

    Write-Host "Activating environment and installing binary packages (pyarrow, onnxruntime, pytorch)..."
    # Use conda run to avoid relying on shell activation behavior
    conda run -n $EnvName --no-capture-output python -m pip install --upgrade pip setuptools wheel

    # Install pyarrow and onnxruntime from conda-forge
    conda install -n $EnvName -c conda-forge pyarrow onnxruntime -y || ExitWith 3 "Failed to install pyarrow/onnxruntime via conda."

    # Install CPU-only PyTorch via pytorch channel (works on many Windows setups)
    conda install -n $EnvName -c pytorch pytorch cpuonly -y || Write-Host "Warning: installing pytorch via conda failed; you'll need to install pytorch manually for your platform."

    Write-Host "Now pip-installing remaining mlops requirements (using --no-deps because heavy binaries are installed via conda)..."
    conda run -n $EnvName --no-capture-output python -m pip install -r mlops\requirements.txt --no-deps || ExitWith 4 "pip install of mlops requirements failed. Check the output above."

    Write-Host "Installation complete. To activate the environment run:"
    Write-Host "    conda activate $EnvName"
    Write-Host "Then you can run the example server inside the env:"
    Write-Host "    python -m mlops.examples.fastapi_server"
    exit 0
} else {
    ExitWith 1 "conda executable not available."
}
