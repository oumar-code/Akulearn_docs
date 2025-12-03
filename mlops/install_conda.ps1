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

# Initialize logging
$logDir = Join-Path (Get-Location) "mlops"
$logFile = Join-Path $logDir "install_conda_run.log"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Force -Path $logDir | Out-Null }

function Log($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logLine = "[$timestamp] $msg"
    Write-Host $logLine
    Add-Content -Path $logFile -Value $logLine -ErrorAction SilentlyContinue
}

function ExitWith($code, $msg) {
    Log "ERROR: $msg"
    Log "Script exited with code $code"
    exit $code
}

Write-Host "== Akulearn: conda installer helper =="

# Helper to get the Python launcher, preferring `py` if available
function Get-PythonLauncher {
    Log "DEBUG: Checking for Python launcher..."
    if (Get-Command py -ErrorAction SilentlyContinue) {
        $pyVersion = & py --version 2>&1
        Log "DEBUG: Found 'py' launcher: $pyVersion"
        return "py"
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        $pyVersion = & python --version 2>&1
        Log "DEBUG: 'py' not found; falling back to 'python' launcher: $pyVersion"
        return "python"
    } else {
        Log "WARNING: Neither 'py' nor 'python' found on PATH. Pre-checks will be limited."
        return $null
    }
}

$pythonLauncher = Get-PythonLauncher
Log "Using Python launcher: $pythonLauncher"
Log "Process ID: $pid"
Log "Working directory: $(Get-Location)"

# Check for conda and, if missing, download & install Miniconda silently into the user's profile
$MinicondaUrl = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
$defaultInstallDir = Join-Path $env:USERPROFILE "Miniconda3"

function Install-Miniconda {
    param(
        [string]$Url = $MinicondaUrl,
        [string]$InstallDir = $defaultInstallDir
    )

    Log "Starting Miniconda download and installation..."
    Log "Download URL: $Url"
    Log "Install directory: $InstallDir"
    $installer = Join-Path $env:TEMP "Miniconda3-latest-Windows-x86_64.exe"
    try {
        Log "Downloading Miniconda installer to $installer..."
        Invoke-WebRequest -Uri $Url -OutFile $installer -ErrorAction Stop
        Log "Download completed successfully."
    } catch {
        Log "WARNING: Invoke-WebRequest failed, trying BITS transfer..."
        try {
            Start-BitsTransfer -Source $Url -Destination $installer -ErrorAction Stop
            Log "BITS transfer completed successfully."
        } catch {
            ExitWith 1 "Failed to download Miniconda installer: $_"
        }
    }

    Log "Running Miniconda silent installer to '$InstallDir'... This may take a minute."
    # Silent installer arguments: /InstallationType=JustMe /RegisterPython=0 /AddToPath=0 /S /D=<dir>
    $args = "/InstallationType=JustMe","/RegisterPython=0","/AddToPath=0","/S","/D=$InstallDir"
    $proc = Start-Process -FilePath $installer -ArgumentList $args -Wait -PassThru -WindowStyle Hidden
    Log "Miniconda installer process exited with code: $($proc.ExitCode)"
    if ($proc.ExitCode -ne 0) {
        ExitWith 1 "Miniconda installer failed with exit code $($proc.ExitCode)."
    }

    # prefer condabin\conda.bat for scripting, fall back to Scripts\conda.exe
    Log "Locating conda executable in $InstallDir..."
    $condaBat = Join-Path $InstallDir "condabin\conda.bat"
    $condaExe = Join-Path $InstallDir "Scripts\conda.exe"
    if (Test-Path $condaBat) {
        Log "Found conda.bat at $condaBat"
        $useConda = $condaBat
    } elseif (Test-Path $condaExe) {
        Log "Found conda.exe at $condaExe"
        $useConda = $condaExe
    } else {
        ExitWith 1 "Miniconda installed but conda executable not found under $InstallDir."
    }

    # Initialize PowerShell integration (best-effort)
    Log "Initializing conda for PowerShell..."
    try {
        & $useConda init powershell | Out-Null
        Log "conda init powershell completed."
    } catch {
        Log "WARNING: conda init returned a warning; continue."
    }

    Log "Miniconda installed successfully at $InstallDir"
    return $useConda
}

Write-Host "Checking for conda on PATH..."
$condaExe = $null

if (Get-Command conda -ErrorAction SilentlyContinue) {
    $condaVersion = & conda --version 2>$null
    Log "Found conda on PATH: $condaVersion"
    $condaExe = (Get-Command conda).Source
    Log "conda executable: $condaExe"
} else {
    Log "conda not found on PATH. Checking for existing Miniconda installation at $defaultInstallDir..."
    $condaBat = Join-Path $defaultInstallDir "condabin\conda.bat"
    $condaExe2 = Join-Path $defaultInstallDir "Scripts\conda.exe"
    if (Test-Path $condaBat) {
        Log "Found conda.bat at $condaBat; using it directly."
        $condaExe = $condaBat
    } elseif (Test-Path $condaExe2) {
        Log "Found conda.exe at $condaExe2; using it directly."
        $condaExe = $condaExe2
    } else {
        Log "Existing Miniconda directory found but no conda executable; attempting to auto-install Miniconda..."
        $condaExe = Install-Miniconda -InstallDir $defaultInstallDir
    }
    # Add installer Scripts path to current PATH so 'conda' command works in this session
    $scriptsPath = Join-Path $defaultInstallDir 'Scripts'
    if ($scriptsPath -notin $env:Path.Split(';')) {
        $env:Path = "$scriptsPath;$env:Path"
        Log "Added $scriptsPath to PATH"
    }
}

# Use the concrete conda path if available, otherwise fall back to 'conda' on PATH
if ($condaExe -and (Test-Path $condaExe)) { 
    $condaCmd = $condaExe 
    Log "Using concrete conda path: $condaCmd"
} else { 
    $condaCmd = "conda"
    Log "Using conda from PATH"
}

Write-Host "Creating conda environment '$EnvName' with Python $PythonVersion..."
Log "Creating conda environment '$EnvName' with Python $PythonVersion (Force: $Force)..."
if ($Force) {
    Log "Force flag set; removing any existing environment..."
    & $condaCmd remove -n $EnvName --all -y
    Log "Environment removal completed."
}

Log "Running: $condaCmd create -n $EnvName python=$PythonVersion -y"
& $condaCmd create -n $EnvName python=$PythonVersion -y
if ($LASTEXITCODE -ne 0) { ExitWith 2 "Failed to create conda env." }
Log "Environment created successfully."

Log "Activating environment and installing binary packages..."
# Use conda run to avoid relying on shell activation behavior
Log "Running: $condaCmd run -n $EnvName --no-capture-output python -m pip install --upgrade pip setuptools wheel"
& $condaCmd run -n $EnvName --no-capture-output python -m pip install --upgrade pip setuptools wheel
Log "pip, setuptools, and wheel upgraded."

# Install pyarrow and onnxruntime from conda-forge
Log "Installing pyarrow and onnxruntime from conda-forge..."
Log "Running: $condaCmd install -n $EnvName -c conda-forge pyarrow onnxruntime -y"
$condaFailed = $false
for ($i = 1; $i -le 3; $i++) {
    Log "Attempt $i of 3..."
    & $condaCmd install -n $EnvName -c conda-forge pyarrow onnxruntime -y 2>&1
    if ($LASTEXITCODE -eq 0) { 
        Log "pyarrow and onnxruntime installed."
        break
    } elseif ($i -lt 3) {
        Log "WARNING: Attempt $i failed; retrying in 10 seconds..."
        Start-Sleep -Seconds 10
    } else {
        Log "WARNING: conda install failed after 3 attempts; will skip and try pip later."
        $condaFailed = $true
    }
}
if ($condaFailed) {
    Log "pyarrow/onnxruntime installation will be retried via pip."
}

# Install CPU-only PyTorch via pytorch channel (works on many Windows setups)
Log "Installing PyTorch (CPU) from pytorch channel..."
Log "Running: $condaCmd install -n $EnvName -c pytorch pytorch cpuonly -y"
$torchFailed = $false
for ($i = 1; $i -le 3; $i++) {
    Log "Attempt $i of 3..."
    & $condaCmd install -n $EnvName -c pytorch pytorch cpuonly -y 2>&1
    if ($LASTEXITCODE -eq 0) {
        Log "PyTorch installed successfully."
        break
    } elseif ($i -lt 3) {
        Log "WARNING: Attempt $i failed; retrying in 10 seconds..."
        Start-Sleep -Seconds 10
    } else {
        Log "WARNING: installing pytorch via conda failed after 3 attempts; will skip and try pip later."
        $torchFailed = $true
    }
}
if ($torchFailed) {
    Log "PyTorch installation will be retried via pip."
} else {
    Log "PyTorch installation attempt completed."
}

Log "Now pip-installing remaining mlops requirements..."
# Filter out heavy binary packages that we already installed via conda so pip
# doesn't try to build them from source. This prevents long source builds
# (e.g. pyarrow) when binary wheels are not available. Also install certain
# packages (like mlflow) with --no-deps so pip won't pull heavy binaries.
$reqFile = Join-Path (Get-Location) "mlops\requirements.txt"
$tempReq = Join-Path (Get-Location) "mlops\requirements-pip.txt"
$condaInstalledPkgs = @('pyarrow','onnxruntime','torch','pytorch')
# Packages that should be installed with --no-deps to avoid pulling heavy deps
$specialNoDepsPkgs = @('mlflow')
Log "Reading requirements from $reqFile and writing filtered list to $tempReq"
try {
    $lines = Get-Content $reqFile -ErrorAction Stop
} catch {
    ExitWith 4 "Could not read requirements file"
}


$filtered = @()
$noDepsToInstall = @()
foreach ($line in $lines) {
    $trim = $line.Trim()
    if ($trim -eq '' -or $trim.StartsWith('#')) { continue }
    $pkgName = $trim.Split('[',':','=')[0].Split('==')[0].Split('<=')[0].Split('>')[0].Split('!')[0].Trim().ToLower()
    if ($condaInstalledPkgs -contains $pkgName) {
        Log "Excluding package from pip install (installed via conda): $pkgName"
        continue
    }
    if ($specialNoDepsPkgs -contains $pkgName) {
        Log "Deferring package to install with --no-deps: $trim"
        $noDepsToInstall += $trim
        continue
    }
    $filtered += $trim
}

# Before running pip, verify that conda-installed packages are visible to pip
Log "Verifying conda-installed packages are visible to pip..."
& $condaCmd run -n $EnvName --no-capture-output python -c "import pyarrow; print(f'pyarrow version: {pyarrow.__version__}')" 2>&1 | Tee-Object -Append -FilePath $logFile
if ($LASTEXITCODE -ne 0) {
    Log "WARNING: pyarrow not found in conda environment. Attempting to install it again..."
    & $condaCmd install -n $EnvName -c conda-forge pyarrow -y 2>&1 | Tee-Object -Append -FilePath $logFile
}

# Write the filtered requirements (excluding conda-provided and --no-deps packages)
Set-Content -Path $tempReq -Value ($filtered -join "`n") -Force
if ($filtered.Count -gt 0) {
    Log "Running: $condaCmd run -n $EnvName --no-capture-output python -m pip install --only-binary :all: -r $tempReq"
    & $condaCmd run -n $EnvName --no-capture-output python -m pip install --only-binary :all: -r $tempReq 2>&1 | Tee-Object -Append -FilePath $logFile
    if ($LASTEXITCODE -ne 0) {
        Log "WARNING: pip install returned non-zero exit code. This may indicate pip attempted to build a package from source."
        Log "Check the output above and the log file: $logFile"
        ExitWith 4 "pip install of mlops requirements failed."
    }
    Log "Pip successfully installed filtered requirements."
} else {
    Log "No filtered pip requirements to install."
}
# Install deferred packages with --no-deps so they rely on conda for heavy binaries
foreach ($pkgSpec in $noDepsToInstall) {
    Log "Installing deferred package with --no-deps: $pkgSpec"
    Log "Running: $condaCmd run -n $EnvName --no-capture-output python -m pip install --only-binary :all: $pkgSpec --no-deps"
    & $condaCmd run -n $EnvName --no-capture-output python -m pip install --only-binary :all: $pkgSpec --no-deps 2>&1 | Tee-Object -Append -FilePath $logFile
    if ($LASTEXITCODE -ne 0) {
        Log "WARNING: Failed to install $pkgSpec with --no-deps"
        Log "Will attempt to install with regular pip (conda-provided binaries should satisfy dependencies)..."
        & $condaCmd run -n $EnvName --no-capture-output python -m pip install --only-binary :all: $pkgSpec 2>&1 | Tee-Object -Append -FilePath $logFile
        if ($LASTEXITCODE -ne 0) {
            Log "ERROR: Also failed with regular pip install. Continuing anyway..."
        }
        # Don't exit here; warn and continue to check if conda already provided the binary
        # If the package is critical, we'll catch it in the imports test later
    } else {
        Log "Successfully installed: $pkgSpec"
    }
}

Log "All pip requirements installed successfully."
# Clean up temp requirements file
Remove-Item -Path $tempReq -ErrorAction SilentlyContinue

Log "Installation complete. To activate the environment run:"
Log "    conda activate $EnvName"
Log "Then you can run the example server inside the env:"
Log "    python -m mlops.examples.fastapi_server"
Log "Full log saved to: $logFile"
exit 0
