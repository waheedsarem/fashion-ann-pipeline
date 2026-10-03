$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'Python 3.12 must be installed and available on PATH.' }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
$env:PATH = "$PSScriptRoot\.venv\Scripts;$env:PATH"
dvc repro
if ($LASTEXITCODE -ne 0) { throw 'DVC pipeline failed.' }
python verify_pipeline.py
if ($LASTEXITCODE -ne 0) { throw 'Pipeline verification failed.' }
