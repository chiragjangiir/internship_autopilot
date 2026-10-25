"""Generates five fake 'screenshots' (HTML mockups). All names and addresses are fictional (example.com)."""
from icons import icon_uri

CHROME = """
body{width:1600px;height:VH;background:linear-gradient(135deg,#c7d2fe,#e0f2fe 45%,#fae8ff);display:grid;place-items:center}
.win{width:1480px;border-radius:14px;overflow:hidden;box-shadow:0 30px 80px rgba(15,23,42,.25),0 0 0 1px rgba(15,23,42,.08);background:#fff}
.bar{height:52px;display:flex;align-items:center;gap:10px;padding:0 18px;background:#f1f5f9;border-bottom:1px solid #e2e8f0;font-size:14px;color:#334155}
.dots{display:flex;gap:8px;margin-right:12px}.dots i{width:13px;height:13px;border-radius:50%;background:#ff5f57}.dots i:nth-child(2){background:#febc2e}.dots i:nth-child(3){background:#28c840}
.bar img{width:22px;height:22px}.bar b{font-weight:600}.bar .sp{flex:1}
.chip{display:inline-block;padding:3px 10px;border-radius:99px;font-size:12.5px;font-weight:600}
.new{background:#e0f2fe;color:#0369a1}.drafted{background:#f1f5f9;color:#475569}.approved{background:#fef3c7;color:#92400e}.sent{background:#dcfce7;color:#166534}.replied{background:#ede9fe;color:#5b21b6}.follow{background:#ffe4e6;color:#9f1239}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
"""

def page(name, h, body, css=""):
    open(f"{name}.html", "w").write(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>{CHROME.replace("VH", f"{h}px")}{css}</style></head><body>{body}</body></html>')

def bar(icons, title, right=""):
    imgs = "".join(f'<img src="{icon_uri(i)}">' for i in icons)
    return f'<div class="bar"><div class="dots"><i></i><i></i><i></i></div>{imgs}<b>{title}</b><span class="sp"></span>{right}</div>'

TARGETS = [
    ("Northwind Robotics", "Dr. Ada Rivera", "a.rivera@northwind.example.com", "northwind.example.com/team", "EN", "Grasp planning for warehouse arms", "replied"),
    ("Lumen Vision Lab", "Prof. Lena Okafor", "okafor@lumenlab.example.com", "lumenlab.example.com/people", "EN", "Event cameras, matches my SLAM project", "replied"),
    ("Harbor AI", "Sam Patel", "careers@harborai.example.com", "harborai.example.com/jobs", "EN", "Open ML intern role, Python + ROS", "replied"),
    ("Bluefin Autonomy", "Dr. Jonas Weber", "j.weber@bluefin.example.com", "bluefin.example.com/research", "DE", "Underwater navigation, Kalman filters", "drafted"),
    ("Cedar Imaging Group", "Mia Chen", "mia.chen@cedar.example.com", "cedar.example.com/about", "EN", "Medical image segmentation", "follow"),
    ("Quill Data Studio", "Tomas Novak", "hello@quill.example.com", "quill.example.com/contact", "EN", "Small team, data viz internships", "approved"),
    ("Orbit Sensors", "Recruiting team", "info@orbit.example.com", "orbit.example.com/careers", "EN", "Sensor fusion, posted intern call", "sent"),
    ("Atlas Field Robotics", "Prof. Ines Duarte", "duarte@atlasfr.example.com", "atlasfr.example.com/lab", "EN", "Agricultural robots, outdoor perception", "new"),
]
LABEL = {"follow": "follow up"}

# 1. targets.csv in a spreadsheet
rows = "".join(f'<tr><td class="rn">{i+2}</td><td><b>{o}</b></td><td>{p}</td><td class="mono">{e}</td><td class="mono url">https://{u}</td><td>{l}</td><td>{w}</td><td><span class="chip {s}">{LABEL.get(s, s)}</span></td></tr>' for i, (o, p, e, u, l, w, s) in enumerate(TARGETS))
page("mock_targets", 820, f'''<div class="win">{bar(["microsoft_excel"], "targets.csv", '<span style="color:#64748b">8 rows · allow list source</span>')}
<div class="fx"><span class="mono">fx</span> why_it_fits</div>
<table><tr class="cols"><td class="rn"></td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td>G</td></tr>
<tr class="hd"><td class="rn">1</td><td>organisation</td><td>person</td><td>email</td><td>source_url</td><td>lang</td><td>why_it_fits</td><td>status</td></tr>{rows}</table></div>''',
""".fx{padding:10px 18px;border-bottom:1px solid #e2e8f0;font-size:14px;color:#475569}.fx span{color:#16a34a;font-weight:700;margin-right:12px}
table{border-collapse:collapse;width:100%;font-size:14.5px}td{border:1px solid #e5e7eb;padding:12px 12px;white-space:nowrap}
.rn{background:#f8fafc;color:#94a3b8;text-align:center;width:44px;font-size:12px}.cols td{background:#f8fafc;color:#94a3b8;text-align:center;font-size:12px;padding:5px}
.hd td{font-weight:700;background:#f0fdf4;color:#166534;border-bottom:2px solid #86efac}.hd .rn{color:#94a3b8;font-weight:400}.url{color:#2563eb}.hd .rn{background:#f8fafc}""")

# 2. draft preview: Mail compose + assistant approval panel
SENTENCES = [
    "I enjoyed your studio's case study on the energy use dashboard, especially how you made hourly data readable on a phone.",
    "In my DATA_VIZ_PROJECT I built a similar dashboard in Python and D3 and reworked it after feedback from real users.",
    "I am a YOUR_YEAR student in YOUR_PROGRAMME and I am looking for an internship from YOUR_START_DATE.",
    "Would your team have room for an intern?",
    "My CV is attached.",
]
OPT_OUT = "If you'd rather not hear from me again, just reply “no thanks” and I won't follow up."
WORDS = len(("Dear Tomas, " + " ".join(SENTENCES) + " Kind regards, YOUR_NAME " + OPT_OUT).split())
body = ("Dear Tomas,<br><br>" + " ".join(SENTENCES[:2]) + "<br><br>" + " ".join(SENTENCES[2:]) +
        f'<br><br>Kind regards,<br>YOUR_NAME<br><span style="color:#94a3b8">{OPT_OUT}</span>')
page("mock_draft", 790, f'''<div class="win">{bar(["apple_mail"], "Internship request · data visualisation (Draft)")}
<div class="split"><div class="mail">
<div class="f"><span>From:</span>YOUR_NAME &lt;you@example.com&gt;</div>
<div class="f"><span>To:</span>Tomas Novak &lt;hello@quill.example.com&gt;</div>
<div class="f"><span>Subject:</span><b>Internship request · data visualisation</b></div>
<div class="att"><img src="{icon_uri("pdf")}"><div><b>CV_YOUR_NAME_current.pdf</b><br><span>142 KB · current CV</span></div></div>
<div class="body">{body}</div></div>
<div class="chat"><div class="who"><img src="{icon_uri("claude")}"><b>Assistant</b></div>
<div class="msg">Preview <b>1 of 1</b> is ready.<ul><li>{WORDS} words (limit 170)</li><li>Detail: their energy use dashboard case study</li><li>Project: DATA_VIZ_PROJECT</li><li>Claims checker: <b class="ok">all {len(SENTENCES)} sentences match facts file</b></li><li>Opt out line: included</li><li>Attachment: current CV only</li></ul>Reply <code>send</code>, <code>edit</code> or <code>skip</code>.</div>
<div class="me">send</div><div class="msg small">Approved. Queued for Apple Mail, then I will check the Sent folder.</div></div></div></div>''',
""".split{display:grid;grid-template-columns:1fr 470px;min-height:640px}.mail{padding:8px 34px 30px}
.f{padding:13px 0;border-bottom:1px solid #f1f5f9;font-size:15px;color:#0f172a}.f span{display:inline-block;width:80px;color:#94a3b8}
.att{display:inline-flex;gap:12px;align-items:center;margin:18px 0 6px;padding:10px 16px;border:1px solid #e2e8f0;border-radius:12px;background:#f8fafc;font-size:14px}.att img{width:34px}.att span{color:#64748b;font-size:12.5px}
.body{font-size:16px;line-height:1.65;color:#1e293b;margin-top:16px;max-width:820px}
.chat{background:#f8fafc;border-left:1px solid #e2e8f0;padding:24px}.who{display:flex;gap:10px;align-items:center;font-size:15px;margin-bottom:16px}.who img{width:28px}
.msg{background:#fff;border:1px solid #e2e8f0;border-radius:16px 16px 16px 4px;padding:16px 18px;font-size:15px;line-height:1.55;color:#1e293b}
.msg ul{margin:10px 0 10px 18px}.msg li{margin:3px 0}.ok{color:#16a34a}code{background:#fef3c7;color:#92400e;padding:2px 7px;border-radius:6px;font-weight:700}
.me{margin:16px 0 16px auto;width:max-content;background:#d97706;color:#fff;font-weight:700;padding:10px 20px;border-radius:16px 16px 4px 16px;font-size:16px}.small{font-size:14px}""")

# 3. sent_log on the Windows PC (PowerShell)
log = [("2026/10/09 10:41:03", "info@orbit.example.com", "Orbit Sensors", "sent", "Outlook"),
       ("2026/10/14 09:02:11", "a.rivera@northwind.example.com", "Northwind Robotics", "sent", "Outlook"),
       ("2026/10/14 09:07:48", "okafor@lumenlab.example.com", "Lumen Vision Lab", "sent", "Outlook"),
       ("2026/10/14 09:13:30", "mia.chen@cedar.example.com", "Cedar Imaging Group", "sent", "Outlook"),
       ("2026/10/14 09:16:55", "careers@harborai.example.com", "Harbor AI", "sent", "Outlook")]
lines = "".join(f"<div>{','.join(r)}</div>" for r in log)
page("mock_sentlog", 860, f'''<div class="win ps">{bar(["powershell"], "Windows PowerShell · spare PC (via SSH)")}
<pre class="mono"><span class="p">PS C:\\autopilot&gt;</span> .\\send_drafts.ps1 .\\only_list.txt 100 Send
<span class="i">[09:02:04]</span> Removed stale output file dry_run.txt
<span class="i">[09:02:04]</span> Only list: 5 addresses, already in sent_log: 1, STOP file: <span class="g">absent</span>, mode: Send
<span class="i">[09:02:11]</span> <span class="g">SENT</span>  a.rivera@northwind.example.com  (1/100)
<span class="i">[09:02:11]</span> next in 5 m 37 s
<span class="i">[09:07:48]</span> <span class="g">SENT</span>  okafor@lumenlab.example.com  (2/100)
<span class="i">[09:07:48]</span> next in 5 m 42 s
<span class="i">[09:13:30]</span> <span class="g">SENT</span>  mia.chen@cedar.example.com  (3/100)
<span class="i">[09:13:30]</span> next in 3 m 25 s
<span class="i">[09:16:55]</span> <span class="g">SENT</span>  careers@harborai.example.com  (4/100)
<span class="i">[09:16:56]</span> <span class="y">SKIP</span>  info@orbit.example.com  already in sent_log.csv (2026/10/09)
<span class="i">[09:16:56]</span> Done. 4 sent, 1 skipped, 0 errors.

<span class="p">PS C:\\autopilot&gt;</span> type .\\sent_log.csv
<span class="h">timestamp,email,organisation,status,client</span>
{lines}</pre></div>''',
""".ps{background:#012456}.ps .bar{background:#e2e8f0}
pre{padding:26px 30px 34px;color:#e2e8f0;font-size:15.5px;line-height:1.7;white-space:pre}pre div{white-space:pre}
.p{color:#fde047}.i{color:#7dd3fc}.g{color:#4ade80;font-weight:700}.y{color:#fbbf24;font-weight:700}.h{color:#94a3b8}""")

# 4. calendar week view
days = ["Mon 19", "Tue 20", "Wed 21", "Thu 22", "Fri 23"]
EV = [  # day, start hour, duration h, title, kind
    (0, 10, 1, "[INT] Lumen Vision Lab · call with Prof. Okafor", "int"),
    (1, 14, .75, "[PREP] Lumen follow up notes", "prep"),
    (2, 9, 1.5, "[INT] Harbor AI · technical interview", "int"),
    (3, 17, 1, "[DL] Cedar Imaging · application deadline", "dl"),
    (4, 11, 1, "[INT] Northwind Robotics · team chat", "int"),
]
hours = range(8, 19)
evs = "".join(f'<div class="ev {k}" style="left:calc({d}*20% + 4px);top:{(h-8)*62+2}px;height:{du*62-6}px"><b>{t}</b><span>{int(h):02d}:{int((h%1)*60):02d}</span></div>' for d, h, du, t, k in EV)
grid = "".join(f'<div class="hr"><span>{h:02d}:00</span></div>' for h in hours)
page("mock_calendar", 900, f'''<div class="win">{bar(["apple_calendar"], "Calendar · Week 43, October 2026", '<span class="chip int">[INT] interview</span>&nbsp;<span class="chip dl">[DL] deadline</span>&nbsp;<span class="chip prep">[PREP] preparation</span>')}
<div class="cal"><div class="days"><div></div>{"".join(f"<div>{d}</div>" for d in days)}</div>
<div class="body"><div class="hours">{grid}</div><div class="cols">{evs}
<div class="pop"><b>[INT] Harbor AI · technical interview</b><div class="t">Wed 21 Oct · 09:00 to 10:30 · video call</div>
<div class="al"><img src="{icon_uri("bell", "#d97706")}">Alerts</div><ul><li>1 day before</li><li>1 hour before</li><li>30 minutes before</li><li>15 minutes before</li></ul>
<div class="t">Notes: prepare ROS 2 demo, read their latest blog post. Logged in status.md.</div></div></div></div></div></div>''',
""".chip.int{background:#ede9fe;color:#5b21b6}.chip.dl{background:#ffe4e6;color:#9f1239}.chip.prep{background:#e0f2fe;color:#0369a1}
.days{display:grid;grid-template-columns:70px repeat(5,1fr);border-bottom:1px solid #e2e8f0}.days div{padding:14px;font-weight:700;font-size:15px;color:#334155}
.body{display:grid;grid-template-columns:70px 1fr;position:relative}.hr{height:62px;border-bottom:1px solid #f1f5f9;font-size:12px;color:#94a3b8;padding:4px 10px}
.cols{position:relative;background:repeating-linear-gradient(90deg,transparent 0 calc(20% - 1px),#f1f5f9 calc(20% - 1px) 20%),repeating-linear-gradient(transparent 0 61px,#f1f5f9 61px 62px)}
.ev{position:absolute;width:calc(20% - 8px);border-radius:8px;padding:6px 10px;font-size:13px;overflow:hidden;border-left:4px solid}.ev b{display:block;font-weight:600;line-height:1.3}.ev span{font-size:12px;opacity:.75}
.ev.int{background:#ede9fe;color:#4c1d95;border-color:#7c3aed}.ev.dl{background:#ffe4e6;color:#881337;border-color:#e11d48}.ev.prep{background:#e0f2fe;color:#075985;border-color:#0284c7}
.pop{position:absolute;left:calc(40% + 30px);top:110px;width:360px;background:#fff;border-radius:14px;box-shadow:0 20px 50px rgba(15,23,42,.22),0 0 0 1px #e2e8f0;padding:18px 20px;font-size:14px;color:#1e293b;z-index:2}
.pop .t{color:#64748b;margin:6px 0}.al{display:flex;gap:8px;align-items:center;font-weight:700;margin-top:10px}.al img{width:18px}.pop ul{margin:6px 0 8px 22px;line-height:1.6}""")

# 5. status.md rendered
page("mock_status", 980, f'''<div class="win">{bar(["markdown"], "status.md · preview")}
<div class="md"><h1>Internship search · status</h1><p class="m">Updated 2026/10/21 08:40 by the assistant · source of truth for meetings and decisions</p>
<h2>Pipeline</h2><div class="kpi"><div><b>8</b>targets</div><div><b>5</b>sent</div><div><b>3</b>replied</div><div><b>3</b>meetings booked</div><div><b>1</b>follow up</div></div>
<h2>Meetings</h2><table><tr><th>Date</th><th>Organisation</th><th>Who</th><th>Type</th><th>Status</th></tr>
<tr><td>Mon 19 Oct 10:00</td><td>Lumen Vision Lab</td><td>Prof. Lena Okafor</td><td>Intro call</td><td><span class="chip sent">done</span></td></tr>
<tr><td>Wed 21 Oct 09:00</td><td>Harbor AI</td><td>Sam Patel</td><td>Technical interview</td><td><span class="chip approved">upcoming</span></td></tr>
<tr><td>Fri 23 Oct 11:00</td><td>Northwind Robotics</td><td>Dr. Ada Rivera</td><td>Team chat</td><td><span class="chip approved">upcoming</span></td></tr></table>
<h2>Decision log</h2><ul class="log">
<li><span class="mono">2026/10/19</span> Lumen asked for a one page project summary. <b>Decision:</b> send summary by Wed, reuse facts file only.</li>
<li><span class="mono">2026/10/18</span> Cedar replied out of office until 2 Nov. <b>Decision:</b> added to follow up list, no reply now.</li>
<li><span class="mono">2026/10/17</span> Bluefin draft failed claims check (“led a team of ten”). <b>Decision:</b> sentence removed, not in facts file.</li></ul></div></div>''',
""".md{padding:34px 60px 44px;color:#1e293b}.md h1{font-size:32px;letter-spacing:-.02em;border-bottom:1px solid #e2e8f0;padding-bottom:10px}.m{color:#64748b;font-size:14px;margin-top:10px}
.md h2{font-size:21px;margin:28px 0 12px}.kpi{display:flex;gap:14px}.kpi div{flex:1;border:1px solid #e2e8f0;border-radius:12px;padding:14px 16px;color:#64748b;font-size:14px}.kpi b{display:block;font-size:28px;color:#0f172a}
table{border-collapse:collapse;width:100%;font-size:15px}th,td{border:1px solid #e2e8f0;padding:10px 14px;text-align:left}th{background:#f8fafc}
.log{margin-left:20px;line-height:1.7;font-size:15px}.log .mono{color:#64748b;margin-right:8px}""")
