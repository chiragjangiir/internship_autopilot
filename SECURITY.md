# Security

## Reporting a problem

If you find a way the scripts could send email without approval, mail the wrong person, or leak personal data, please do not open a public issue. Write to you@example.com (replace this with your own address when you publish) with the steps to reproduce. You will get an answer within a week.

## What is in scope

* bypassing the preview and `send` approval
* sending to an address that is not on the allow list
* sending an address twice despite `sent_log.csv`
* ignoring the STOP file, the daily cap or the pauses
* personal data committed to the repository

## Good practice for users

* Never commit `data/`, real CSV files, CVs or logs. They are in `.gitignore` for a reason.
* The scripts need no passwords or API keys. If a change asks you to add one to a file, do not.
* Reach a sending PC only through a private VPN, never through an open port on the internet.
