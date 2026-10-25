"""Generates workflow.html: 8-step plain-language infographic."""
from icons import icon_uri

steps = [
    ("Find the right people", "The assistant searches the web for companies, labs and professors that match you, plus a real public email.", ["search"], "#2563eb"),
    ("Keep one clean list", "Everyone goes into one spreadsheet with the source link and why they fit. Only names on this list can be mailed.", ["microsoft_excel"], "#0284c7"),
    ("Write a personal email", "A short email (under 170 words) that mentions one real detail of their work and one matching project of yours.", ["claude", "pdf"], "#7c3aed"),
    ("Check every claim", "Each sentence is compared to your facts file. Anything that isn't true or is inflated gets removed.", ["shield_check"], "#e11d48"),
    ("Save as drafts", "Emails are saved as drafts with your current CV attached. Nothing has been sent yet.", ["apple_mail", "microsoft_outlook"], "#64748b"),
    ("You read and say “send”", "You see a preview of every email. Only when you type “send” does anything leave.", ["user_check"], "#d97706"),
    ("Send slowly, then verify", "A few emails at a time with random pauses, a daily limit and a log, then a check that each one really arrived in Sent.", ["send", "mail_check"], "#16a34a"),
    ("Handle replies & meetings", "Replies are summarised with a suggested answer for you to approve. Interviews go into your calendar with reminders.", ["apple_calendar", "markdown"], "#0d9488"),
]

cards = []
for i, (t, d, ics, c) in enumerate(steps, 1):
    imgs = "".join(f'<span class="ic"><img src="{icon_uri(n, c)}"></span>' for n in ics)
    cards.append(f'''<div class="card" style="--c:{c}"><div class="top"><div class="num">{i}</div><div class="icons">{imgs}</div></div>
<h3>{t}</h3><p>{d}</p></div>''')

html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>
body{{width:1600px;height:850px;background:linear-gradient(160deg,#fffbeb,#f0f9ff 60%,#f5f3ff);padding:56px 64px}}
h1{{font-size:40px;font-weight:800;letter-spacing:-.025em}} .sub{{font-size:19px;color:var(--muted);margin-top:8px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:36px 40px;margin-top:44px;position:relative}}
.card{{background:#fff;border-radius:24px;padding:26px 26px 28px;box-shadow:0 10px 30px rgba(15,23,42,.07);border:1px solid #e2e8f0;position:relative;min-height:300px}}
.card:before{{content:"";position:absolute;left:0;top:0;right:0;height:7px;border-radius:24px 24px 0 0;background:var(--c)}}
.card:not(:nth-child(4n)):after{{content:"";position:absolute;right:-31px;top:58px;border:11px solid transparent;border-left:15px solid #cbd5e1}}
.top{{display:flex;align-items:center;justify-content:space-between}}
.num{{width:54px;height:54px;border-radius:50%;background:var(--c);color:#fff;font-size:26px;font-weight:800;display:grid;place-items:center}}
.icons{{display:flex}} .ic{{width:58px;height:58px;border-radius:16px;background:#fff;border:1px solid #e2e8f0;display:grid;place-items:center;margin-left:-10px;box-shadow:0 4px 10px rgba(15,23,42,.06)}}
.ic img{{width:38px;height:38px}}
h3{{font-size:22px;margin:22px 0 10px;letter-spacing:-.01em}} p{{font-size:16.5px;line-height:1.5;color:#475569}}
.card:nth-child(6){{background:#fffbeb;border:2px solid #f59e0b}}
.turn{{position:absolute;right:-28px;top:300px;width:60px;height:68px;border:4px solid #cbd5e1;border-left:none;border-radius:0 34px 34px 0}}
</style></head><body>
<h1>Eight steps, one human decision</h1><div class="sub">What happens from “I need an internship” to “interview booked”. You stay in control at step 6.</div>
<div class="grid">{"".join(cards)}</div></body></html>'''
open("workflow.html", "w").write(html)
