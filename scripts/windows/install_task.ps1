<#
.SYNOPSIS
  Registers a daily Windows scheduled task that runs send_drafts.ps1 in Send mode.

.DESCRIPTION
  Outlook COM needs a signed in desktop session, so the task runs only while your user is logged on.
  Keep the spare PC logged in (screen locked is fine). Remove the task with:
    Unregister-ScheduledTask -TaskName InternshipAutopilot
#>
param(
    [string] $Folder = $PSScriptRoot,
    [string] $At = '09:00',
    [int] $DailyCap = 100
)
$taskArgs = "-NoProfile -ExecutionPolicy Bypass -File `"$Folder\send_drafts.ps1`" `"$Folder\only_list.txt`" $DailyCap Send"
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $taskArgs -WorkingDirectory $Folder
$trigger = New-ScheduledTaskTrigger -Daily -At $At
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
Register-ScheduledTask -TaskName 'InternshipAutopilot' -Action $action -Trigger $trigger -Principal $principal -Force | Out-Null
Write-Host "Task InternshipAutopilot registered: daily at $At, cap $DailyCap, folder $Folder"
Write-Host "Before the first real run: run send_drafts.ps1 in DryRun mode and read dry_run.txt."
