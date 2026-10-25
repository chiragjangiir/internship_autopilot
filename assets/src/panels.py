"""Generates setup.html and faq.html (section openers for the README)."""
from icons import icon_uri

CSS = """body{width:1600px;background:#f8fafc;padding:48px 56px}
h1{font-size:36px;font-weight:800;letter-spacing:-.025em} .sub{color:#64748b;font-size:18px;margin-top:6px}
.grid{display:grid;gap:26px;margin-top:30px}
.card{background:#fff;border-radius:22px;border:1px solid #e2e8f0;box-shadow:0 10px 30px rgba(15,23,42,.06);padding:28px 30px;border-top:7px solid var(--c)}
.logos{display:flex;gap:10px;margin-bottom:16px}.logos span{width:60px;height:60px;border-radius:16px;border:1px solid #e2e8f0;display:grid;place-items:center;background:#fff}.logos img{width:38px;height:38px}
h2{font-size:24px;margin-bottom:6px} .role{color:#64748b;font-size:16px;margin-bottom:16px}
ol{margin-left:22px;font-size:16.5px;line-height:1.55;color:#1e293b} ol li{margin:7px 0} code{font-family:ui-monospace,Menlo,monospace;font-size:14.5px;background:#f1f5f9;padding:2px 7px;border-radius:6px}
"""

def page(name, body):
    open(f"{name}.html", "w").write(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>{CSS}</style></head><body>{body}</body></html>')

def logos(names):
    return '<div class="logos">' + "".join(f'<span><img src="{icon_uri(n)}"></span>' for n in names) + "</div>"

MAC = ["Copy <code>scripts/mac</code> to your Mac and make the scripts executable",
       "Add your sending account to Apple Mail",
       "Allow Terminal to control Mail and Calendar (asked on first run)",
       "Put your facts file and current CV in <code>data/</code>",
       "Send one test email to yourself with <code>send_att.sh</code>"]
WIN = ["Install classic Outlook and sign in to your sending account",
       "Copy <code>scripts/windows</code> to <code>C:\\autopilot</code>",
       "Run a dry run first: <code>send_drafts.ps1 only_list.txt 100 DryRun</code>",
       "Register the daily task with <code>install_task.ps1</code>",
       "Optional: reach the PC over SSH through a private VPN such as Tailscale"]
li = lambda xs: "<ol>" + "".join(f"<li>{x}</li>" for x in xs) + "</ol>"
page("setup", f'''<h1>Setup: pick one sender, or use both</h1><div class="sub">The assistant prepares the same drafts either way. Only the last mile differs.</div>
<div class="grid" style="grid-template-columns:1fr 1fr">
<div class="card" style="--c:#7c3aed">{logos(["apple", "apple_mail", "apple_calendar", "terminal"])}<h2>Mac · Apple Mail</h2><div class="role">Interactive sending, replies in thread, calendar entries</div>{li(MAC)}</div>
<div class="card" style="--c:#2563eb">{logos(["microsoft_windows", "microsoft_outlook", "powershell", "tailscale"])}<h2>Windows PC · Outlook</h2><div class="role">Unattended batches on a spare PC, every day</div>{li(WIN)}</div>
</div>''')

FAQ = [("Does it send anything on its own?", "No. Every email and every reply waits for you to type “send”."),
       ("Is this a mass mailing tool?", "No. It is built for a few personal emails a day, each one written for one person."),
       ("Where do the email addresses come from?", "Only from public pages, with the source link saved. Addresses are never guessed."),
       ("Can it make my CV sound better than it is?", "No. The claims checker removes anything that is not in your facts file."),
       ("Do I need both a Mac and a PC?", "No. Use either sender. The Windows route is only for running batches unattended."),
       ("How do I stop a run right now?", "Create a file called STOP next to the script. Sending halts before the next email.")]
cards = "".join(f'<div class="card" style="--c:#0d9488"><div class="q"><img src="{icon_uri("circle_help", "#0d9488")}"><h2>{q}</h2></div><p>{a}</p></div>' for q, a in FAQ)
page("faq", f'''<h1>Questions people ask first</h1><div class="sub">Short answers here, details in the README.</div>
<div class="grid" style="grid-template-columns:repeat(3,1fr)">{cards}</div>
<style>.q{{display:flex;gap:12px;align-items:flex-start}}.q img{{width:30px;flex:none;margin-top:2px}}.q h2{{font-size:20px;line-height:1.3}}.card p{{font-size:16.5px;line-height:1.5;color:#475569;margin-top:10px}}</style>''')
