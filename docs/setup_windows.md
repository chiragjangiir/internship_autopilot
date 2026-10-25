# Setup on a Windows PC (classic Outlook)

<p align="center"><img src="../assets/images/mock_sentlog.png" alt="A run of send_drafts.ps1" width="100%"></p>

This route is for a spare PC that sends approved drafts every day, even when your laptop is closed.

## 1. Prepare

* Install **classic Outlook** (the new Outlook has no COM interface) and sign in to your sending account.
* Copy `scripts/windows` to `C:\autopilot`.
* Put `only_list.txt` and, if you want organisation names in the log, `targets.csv` in the same folder.
* Windows may block downloaded scripts. Right click each `.ps1` file, open Properties and tick **Unblock**.

## 2. Dry run (the default)

Open PowerShell in `C:\autopilot`:

```powershell
.\send_drafts.ps1 .\only_list.txt 100
```

Nothing is sent. The script deletes any old `dry_run.txt`, then writes a fresh one with every draft it would send. Read it. Only addresses on the only list with exactly one recipient appear.

## 3. Real run

```powershell
.\send_drafts.ps1 .\only_list.txt 100 Send
```

What happens, in order: STOP file check, daily cap check, sent log check, send, a check in Sent Items, a line in `sent_log.csv`, then a random pause of 3 to 8 minutes. Creating a file named `STOP` in the folder halts the run, even during a pause.

## 4. Run it every day

```powershell
.\install_task.ps1
```

This registers a daily task at 09:00 in Send mode with a cap of 100. Outlook COM needs a signed in desktop, so keep the PC logged in (a locked screen is fine). Change the time or cap with the `At` and `DailyCap` parameters of the script.

## 5. Reach the PC from your laptop (optional)

* Turn on the OpenSSH Server feature in Windows Settings, under Optional features.
* Install a private VPN such as Tailscale on both machines, so the PC is never exposed to the internet.
* Connect with `ssh YOUR_USER@YOUR_PC_NAME` and run the commands above.

Keep the host name, user name and VPN details out of this repository.
