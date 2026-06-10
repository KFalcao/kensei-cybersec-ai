# Register a Windows Scheduled Task to run the daily report
# Usage: Open PowerShell as Administrator and run:
#   .\register_task.ps1

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$configPath = Join-Path $scriptDir 'report_config.json'
if (-Not (Test-Path $configPath)) {
    Write-Error "Config not found: $configPath"
    exit 1
}

$config = Get-Content $configPath -Raw | ConvertFrom-Json
$time = $config.time
if (-not $time) { $time = '08:00' }
$taskName = $config.task_name
if (-not $taskName) { $taskName = 'KenseiDailyReport' }

$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) {
    # fall back to python in PATH
    $python = 'python'
}

$runScript = Join-Path $scriptDir 'run_report.py'
$action = "`"$python`" `"$runScript`""

Write-Host "Registering scheduled task '$taskName' to run daily at $time"

# Create or replace the scheduled task
$schtasksArgs = @('/Create', '/SC', 'DAILY', '/TN', $taskName, '/TR', $action, '/ST', $time, '/F')
$proc = Start-Process -FilePath schtasks.exe -ArgumentList $schtasksArgs -NoNewWindow -Wait -PassThru
if ($proc.ExitCode -eq 0) {
    Write-Host "Scheduled task created/replaced successfully."
} else {
    Write-Error "Failed to create scheduled task (exit code $($proc.ExitCode))."
}
