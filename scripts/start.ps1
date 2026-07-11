$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root
Write-Host "Starting backend..."
python -m uv run backend/app/main.py --reload --port 3000
