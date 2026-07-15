$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
Write-Host "Starting backend..."
python -m uv run --directory backend uvicorn app.main:app --reload --port 3000
