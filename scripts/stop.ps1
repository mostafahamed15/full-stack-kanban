$process = Get-Process -Name uv -ErrorAction SilentlyContinue
if ($process) {
  $process | Stop-Process -Force
  Write-Host "Stopped uv process(es)."
} else {
  Write-Host "No uv process found."
}
