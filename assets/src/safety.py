"""Generates safety.html: the seven guard rails every email passes, plus lessons learned."""
from icons import icon_uri

GATES = [  # icon, name, rule, prevents, colour
    ("list_checks", "Allow list", "Only addresses in the only list file can be mailed.", "wrong recipients", "#38bdf8"),
    ("flask_conical", "Dry run", "Old output deleted, then a test run lists who would be mailed.", "stale results", "#a78bfa"),
    ("eye", "Preview", "You read every email. Nothing goes without your “send”.", "unreviewed emails", "#fbbf24"),
    ("history", "Sent log", "sent_log.csv is checked first. Every address is mailed once.", "double emails", "#34d399"),
    ("gauge", "Daily cap", "Hard limit per day (e.g. 100). The run stops at the cap.", "bulk sending", "#f472b6"),
    ("hourglass", "Random delay", "A 3 to 8 minute pause between emails.", "bursts of mail", "#fb923c"),
    ("octagon_x", "STOP switch", "Create a file named STOP and sending halts at once.", "runaway runs", "#f87171"),
]
LESSONS = [
    ("triangle_alert", "Text matching picked the wrong people", "The first run picked companies by name. It was stopped, then replaced by an explicit allow list plus a dry run."),
    ("trash_2", "A stale dry run file looked like a real result", "Output files are now deleted before every run, so what you see is always fresh."),
    ("archive", "An old CV with inflated numbers was still in the folder", "There is now one current CV. Old versions are archived and never attached."),
    ("eye", "Fast is not the same as right", "Preview before send became mandatory, for first emails and for replies."),
]

gates = "".join(f'''<div class="gate" style="--c:{c}"><div class="n">{i}</div><div class="ic"><img src="{icon_uri(ic, c)}"></div>
<h3>{n}</h3><p>{r}</p><div class="stop">stops<br><b>{s}</b></div></div>''' for i, (ic, n, r, s, c) in enumerate(GATES, 1))
lessons = "".join(f'''<div class="l"><img src="{icon_uri(ic, "#fbbf24")}"><div><h4>{h}</h4><p>{t}</p></div></div>''' for ic, h, t in LESSONS)

html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>
body{{width:1600px;height:820px;background:radial-gradient(1200px 500px at 50% 0%,#1e2a6e,#0a1238 70%);color:#e2e8f0;padding:52px 60px}}
h1{{font-size:40px;font-weight:800;letter-spacing:-.025em;color:#fff}} .sub{{color:#94a3b8;font-size:18px;margin-top:8px}}
.track{{position:relative;margin-top:44px;display:flex;align-items:stretch;gap:14px}}
.track:before{{content:"";position:absolute;left:-30px;right:-30px;top:112px;height:6px;border-radius:3px;
 background:linear-gradient(90deg,#38bdf8,#a78bfa,#fbbf24,#34d399,#f472b6,#fb923c,#f87171);box-shadow:0 0 24px rgba(167,139,250,.6)}}
.end{{width:92px;display:flex;flex-direction:column;align-items:center;padding-top:72px;flex:none;position:relative}}
.end .ic{{width:84px;height:84px;border-radius:24px;background:#fff;display:grid;place-items:center;box-shadow:0 0 0 6px rgba(255,255,255,.08)}}
.end .ic img{{width:50px;height:50px}} .end span{{margin-top:12px;font-weight:700;font-size:15px;color:#cbd5e1}}
.gate{{flex:1;position:relative;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:90px 90px 20px 20px;padding:26px 16px 18px;text-align:center;backdrop-filter:blur(2px)}}
.gate:before{{content:"";position:absolute;inset:-1px;border-radius:inherit;border-top:3px solid var(--c);pointer-events:none}}
.n{{position:absolute;top:-14px;left:50%;transform:translateX(-50%);width:30px;height:30px;border-radius:50%;background:var(--c);color:#0a1238;font-weight:800;font-size:15px;display:grid;place-items:center}}
.gate .ic{{width:96px;height:96px;margin:20px auto 0;border-radius:50%;background:#0a1238;border:3px solid var(--c);display:grid;place-items:center;position:relative;z-index:1;box-shadow:0 0 22px color-mix(in srgb,var(--c) 55%,transparent)}}
.gate .ic img{{width:46px;height:46px}}
h3{{font-size:19px;color:#fff;margin:18px 0 8px}} .gate p{{font-size:14.5px;line-height:1.45;color:#cbd5e1;min-height:84px}}
.stop{{margin-top:12px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#94a3b8;border-top:1px dashed rgba(255,255,255,.15);padding-top:10px}}
.stop b{{display:block;font-size:14px;letter-spacing:0;text-transform:none;color:var(--c);margin-top:3px}}
h2{{font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:#fbbf24;margin:46px 0 16px}}
.lessons{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.l{{display:flex;gap:14px;background:rgba(251,191,36,.06);border:1px solid rgba(251,191,36,.25);border-radius:16px;padding:18px}}
.l img{{width:30px;height:30px;flex:none;margin-top:2px}} h4{{font-size:16px;color:#fff;line-height:1.3;margin-bottom:6px}} .l p{{font-size:14px;line-height:1.45;color:#cbd5e1}}
</style></head><body>
<h1>Seven guard rails between a draft and a sent email</h1>
<div class="sub">Every email passes all seven, in this order. If any one says no, the email waits.</div>
<div class="track">
<div class="end"><div class="ic"><img src="{icon_uri("folder_open", "#0b1437")}"></div><span>Draft</span></div>
{gates}
<div class="end"><div class="ic"><img src="{icon_uri("mail_check", "#16a34a")}"></div><span>Sent ✓</span></div>
</div>
<h2>Learned the hard way</h2><div class="lessons">{lessons}</div>
</body></html>'''
open("safety.html", "w").write(html.replace("Sent ✓", "Sent"))
