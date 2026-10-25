<#
.SYNOPSIS
  Sends approved Outlook drafts, but only to addresses on the only list.

.DESCRIPTION
  Guard rails, in the order they run:
    1. Old dry run output is deleted first, so a stale file can never look like a fresh result.
    2. Only drafts with exactly one recipient who is on the only list are considered.
    3. Addresses already in sent_log.csv are skipped. Every address is mailed once.
    4. A daily cap counts everything already sent today.
    5. A STOP file next to the script halts sending before the next email, even during a pause.
    6. A random pause of 3 to 8 minutes separates emails.
  The default mode is DryRun. Nothing is sent unless you pass Send explicitly.

.EXAMPLE
  .\send_drafts.ps1 .\only_list.txt 100            # dry run, writes dry_run.txt
  .\send_drafts.ps1 .\only_list.txt 100 Send       # real run
#>
param(
    [Parameter(Position = 0, Mandatory = $true)] [string] $OnlyList,
    [Parameter(Position = 1)] [int] $DailyCap = 100,
    [Parameter(Position = 2)] [ValidateSet('DryRun', 'Send')] [string] $Mode = 'DryRun',
    [int] $MinPauseSeconds = 180,
    [int] $MaxPauseSeconds = 480,
    [string] $SentLog = (Join-Path $PSScriptRoot 'sent_log.csv'),
    [string] $Targets = (Join-Path $PSScriptRoot 'targets.csv'),
    [string] $StopFile = (Join-Path $PSScriptRoot 'STOP'),
    [string] $DryRunOut = (Join-Path $PSScriptRoot 'dry_run.txt')
)
$ErrorActionPreference = 'Stop'
function Say($text) { Write-Host ("[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $text) }
function Now { Get-Date -Format 'yyyy\/MM\/dd HH:mm:ss' }

if (Test-Path $DryRunOut) { Remove-Item $DryRunOut; Say 'Removed stale output file dry_run.txt' }

$allow = @(Get-Content $OnlyList | ForEach-Object { $_.Trim().ToLower() } | Where-Object { $_ -and -not $_.StartsWith('#') })
$log = @(if (Test-Path $SentLog) { Import-Csv $SentLog })
$already = @{}
foreach ($row in $log) { $already[$row.email.ToLower()] = $row.timestamp }
$orgOf = @{}
if (Test-Path $Targets) { foreach ($t in Import-Csv $Targets) { $orgOf[$t.email.ToLower()] = $t.organisation } }
$today = Get-Date -Format 'yyyy\/MM\/dd'
$sentToday = @($log | Where-Object { $_.timestamp.StartsWith($today) }).Count
$onLog = @($allow | Where-Object { $already.ContainsKey($_) }).Count
$stop = if (Test-Path $StopFile) { 'present' } else { 'absent' }
Say "Only list: $($allow.Count) addresses, already in sent_log: $onLog, STOP file: $stop, mode: $Mode"
if ($stop -eq 'present') { Say 'STOP file present, nothing sent.'; exit 2 }

$outlook = New-Object -ComObject Outlook.Application
$session = $outlook.GetNamespace('MAPI')
$drafts = $session.GetDefaultFolder(16)      # olFolderDrafts
$sentFolder = $session.GetDefaultFolder(5)   # olFolderSentMail

# Copy the items first: sending a draft removes it from the folder while we loop.
$queue = @()
foreach ($item in @($drafts.Items)) {
    if ($item.Recipients.Count -ne 1) { continue }
    # Note: assumes SMTP recipients. Exchange accounts may need PropertyAccessor PR_SMTP_ADDRESS here.
    $addr = $item.Recipients.Item(1).Address.ToLower()
    if ($allow -contains $addr) { $queue += [pscustomobject]@{ Item = $item; Email = $addr; Subject = $item.Subject } }
}
$done = 0; $skipped = 0; $errors = 0
foreach ($q in $queue) {
    if ($already.ContainsKey($q.Email)) { Say "SKIP  $($q.Email)  already in sent_log.csv ($($already[$q.Email].Split(' ')[0]))"; $skipped++; continue }
    if ($sentToday -ge $DailyCap) { Say "Daily cap of $DailyCap reached. Stopping."; break }
    if (Test-Path $StopFile) { Say 'STOP file found. Stopping.'; break }

    if ($Mode -eq 'DryRun') {
        Add-Content $DryRunOut "$($q.Email)`t$($q.Subject)"
        Say "WOULD SEND  $($q.Email)  `"$($q.Subject)`""
        $already[$q.Email] = 'dry run'; $sentToday++; continue
    }
    try {
        $q.Item.Send()
        $status = 'queued'
        for ($i = 0; $i -lt 24 -and $status -eq 'queued'; $i++) {   # up to 2 minutes for the Sent Items check
            Start-Sleep -Seconds 5
            foreach ($m in @($sentFolder.Items.Restrict("[Subject] = '$($q.Subject.Replace("'", "''"))'"))) {
                if ($m.Recipients.Count -ge 1 -and $m.Recipients.Item(1).Address.ToLower() -eq $q.Email) { $status = 'sent' }
            }
        }
        [pscustomobject]@{ timestamp = Now; email = $q.Email; organisation = $orgOf[$q.Email]; status = $status; client = 'Outlook' } |
            Export-Csv $SentLog -Append -NoTypeInformation -Encoding UTF8
        $already[$q.Email] = Now; $sentToday++; $done++
        Say ("{0}  {1}  ({2}/{3})" -f $status.ToUpper(), $q.Email, $sentToday, $DailyCap)
    } catch {
        $errors++; Say "ERROR  $($q.Email)  $($_.Exception.Message)"
    }
    if ($q -ne $queue[-1]) {
        $pause = Get-Random -Minimum $MinPauseSeconds -Maximum ($MaxPauseSeconds + 1)
        Say ("next in {0} m {1} s" -f [math]::Floor($pause / 60), ($pause % 60))
        for ($waited = 0; $waited -lt $pause; $waited += 10) {
            if (Test-Path $StopFile) { break }
            Start-Sleep -Seconds 10
        }
    }
}
Say "Done. $done sent, $skipped skipped, $errors errors."
if ($Mode -eq 'DryRun') { Say "Dry run only. Review dry_run.txt, then run again with Send." }
