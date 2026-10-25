# Sanitisation checklist

What was removed or replaced before this repository was made public, and how to keep it that way.

## Checklist

<table>
<tr><th>Category</th><th>What happened</th><th>Placeholder used</th></tr>
<tr><td>Real names (you, recipients, contacts)</td><td>Removed. Recipients in examples and screenshots are invented people. LICENSE uses only the public GitHub handle aghasalim.</td><td><code>YOUR_NAME</code>, fictional names</td></tr>
<tr><td>Email addresses</td><td>Removed. Every address in the repository ends in <code>example.com</code>.</td><td><code>you@example.com</code></td></tr>
<tr><td>Phone numbers</td><td>None included.</td><td>none needed</td></tr>
<tr><td>IBAN and bank details</td><td>None included.</td><td>none needed</td></tr>
<tr><td>Passport and ID numbers</td><td>None included.</td><td>none needed</td></tr>
<tr><td>Passwords, API keys, tokens</td><td>None included. Scripts use the accounts already signed in to Mail and Outlook, so no secrets are needed.</td><td>none needed</td></tr>
<tr><td>Host names, IP addresses</td><td>Removed from scripts and docs.</td><td><code>YOUR_PC_NAME</code>, <code>YOUR_USER</code></td></tr>
<tr><td>Tailscale names</td><td>Removed. Tailscale is only named as an option.</td><td>none</td></tr>
<tr><td>School and university details</td><td>Removed.</td><td><code>YOUR_SCHOOL</code>, <code>YOUR_PROGRAMME</code>, <code>YOUR_YEAR</code></td></tr>
<tr><td>CV files and old CV versions</td><td>Not in the repository. <code>*.pdf</code> and <code>data/</code> are ignored.</td><td><code>CV_YOUR_NAME_current.pdf</code></td></tr>
<tr><td>Real targets, logs, follow ups</td><td>Not in the repository. Real CSV files and logs are ignored. Only fictional files in <code>examples/</code> are kept.</td><td>example data</td></tr>
<tr><td>Real email texts and replies</td><td>Not included. The example email is written for a fictional studio.</td><td><code>DATA_VIZ_PROJECT</code>, <code>ROBOT_ARM_PROJECT</code></td></tr>
<tr><td>Numbers from the real run</td><td>Kept only as rounded totals (hundreds of emails, about 30 companies, cap of 100, several interviews).</td><td>none</td></tr>
<tr><td>Image metadata</td><td>All images are rendered from code. No photos or real screenshots are included.</td><td>none</td></tr>
</table>

## Check before every push

1. Write your own name, school, city, user names and host names into `private_words.txt` in the repository root, one per line. It is in `.gitignore`.
2. Run the scanner:

   ```bash
   python3 scripts/check_private.py
   ```

   It reports email addresses outside `example.com`, phone numbers, IBANs, IP addresses, Tailscale names, API keys and every word from `private_words.txt`. Fix everything it finds.
3. Look at `git status` and make sure no CSV, PDF or log outside `examples/` is staged.
