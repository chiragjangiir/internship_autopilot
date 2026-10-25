# Instructions for the assistant

Paste this file into your AI assistant's project instructions (for example a `CLAUDE.md` file in your working folder). These rules are the core of the project. The scripts only carry out what these rules allow.

## Hard rules

1. **Never send without approval.** Show a full preview of every email and every reply. Send only after the user types the exact word `send` for that preview.
2. **Never guess an email address.** Use only addresses printed on a public page of the organisation. Save that page as `source_url` in `targets.csv`.
3. **Use only the facts file.** Every claim about the user comes from `data/facts.md`. If a fact is missing, ask. Never round up, never invent numbers, titles, awards or team sizes.
4. **One current CV.** Attach only `data/cv/CV_YOUR_NAME_current.pdf`. Older versions live in `data/cv/archive/` and are never attached.
5. **Only the allow list.** Only addresses in `data/only_list.txt` may receive an email. Add an address there only after the user agreed to that target.
6. **Fresh output only.** Delete old dry run files before every run, and never report a result from a file you did not just create.
7. **Low volume.** Respect the daily cap (default 100) and the random pause of 3 to 8 minutes between emails.

## Research

* Look for companies, labs and professors that match the user's goal and the facts file.
* For each target write one row in `targets.csv`: organisation, person, email, source_url, language, why_it_fits, status.
* `why_it_fits` names one concrete thing: a project, a paper, a product or an open role.
* Start every row with status `new`.

## Writing an email

* Under 170 words. Write in the language of the `language` column.
* Address a named person. Never use "Dear Sir or Madam".
* Mention **one specific detail** of their work and **one matching project** from the facts file.
* End with a small, clear ask and this opt out line: "If you'd rather not hear from me again, just reply “no thanks” and I won't follow up."
* Run `python3 scripts/check_draft.py draft.txt data/facts.md`. Fix every error before the preview.
* Then compare each sentence with the facts file yourself and remove anything that is not supported.
* Save the email as a **draft** in Apple Mail or Outlook with the current CV attached. Set the status to `drafted`.

## Preview and approval

Show the user, for each draft:

* recipient, subject, the full body and the attachment name
* word count, the detail used, the project used, and the claims check result

Then wait. `send` means send this one. `edit` means change it and preview again. `skip` means leave it in Drafts. Anything else means do nothing.

## Sending

* **Mac:** `scripts/mac/send_att.sh`. It refuses addresses already in the sent log and verifies the Sent folder.
* **Windows:** add approved addresses to `only_list.txt`. Run `send_drafts.ps1` in DryRun mode, show the user `dry_run.txt`, and run Send mode only after the user approves that list.
* After a verified send, set the status to `sent`.

## Replies

* Read every reply in full, including quoted text and attachments.
* Give the user a short summary and a drafted answer. Send nothing until the user approves it.
* Send approved replies with `scripts/mac/reply_in_thread.sh` so they stay in the same thread.
* Out of office or "please contact my colleague" replies go into `follow_ups.csv` with the date to try again.
* If someone replies "no thanks" or asks not to be contacted, set the status to `opted_out` and never email them again.

## Calendar and status

* Add every meeting and deadline to Apple Calendar with `scripts/mac/add_event.sh`.
* Title convention: `[INT] Organisation · what` for interviews and calls, `[DL] Organisation · what` for deadlines, `[PREP] Organisation · what` for preparation.
* Four alerts on every event: 1 day, 1 hour, 30 minutes and 15 minutes before.
* Log every meeting and every decision in `data/status.md`, newest decision first.
