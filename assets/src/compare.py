"""Generates compare.html: generic vs tailored email, with numbered highlights."""
from icons import icon_uri

def mark(n, text, kind):
    return f'<span class="hl {kind}">{text}<sup>{n}</sup></span>'

bad = lambda n, t: mark(n, t, "bad")
good = lambda n, t: mark(n, t, "good")

GENERIC = f"""<p>{bad(1, "Dear Sir/Madam,")}</p>
<p>{bad(2, "I am writing to apply for any internship position at your company.")} I am a hardworking, passionate and motivated student with excellent communication skills.</p>
<p>{bad(3, "I have led many large projects and improved efficiency by 300%.")} I am sure I would be a great asset to your team.</p>
<p>Please find my CV attached. I look forward to hearing from you.</p>
<p>Best regards,<br>YOUR_NAME</p>"""
GENERIC_ATT = "CV_final_v3_OLD.pdf"
GENERIC_NOTES = [
    (1, "No name: it could be sent to anyone"),
    (2, "No detail about their work, no specific ask"),
    (3, "Inflated claim that isn't in the facts file"),
    (4, "Old CV attached, no opt out line"),
]

TAILORED = f"""<p>{good(1, "Dear Tomas,")}</p>
<p>{good(2, "I enjoyed your studio's case study on the energy use dashboard,")} especially how you made hourly data readable on a phone. {good(3, "In my DATA_VIZ_PROJECT I built a similar dashboard in Python and D3")} and reworked it after feedback from real users.</p>
<p>I am a YOUR_YEAR student in YOUR_PROGRAMME and I am looking for an internship from YOUR_START_DATE. {good(4, "Would your team have room for an intern?")} My CV is attached.</p>
<p>Kind regards,<br>YOUR_NAME<br>{good(5, "If you'd rather not hear from me again, just reply “no thanks”.")}</p>"""
TAILORED_ATT = "CV_YOUR_NAME_current.pdf"
TAILORED_NOTES = [
    (1, "A real person, found on their public page"),
    (2, "One specific detail of their work"),
    (3, "One matching project, checked against the facts file"),
    (4, "A clear, small ask"),
    (5, "Easy opt out, current CV only"),
]

SCORE = [("Addressed to a named person", 0, 1), ("Mentions their actual work", 0, 1), ("Every claim is in the facts file", 0, 1),
         ("Under 170 words", 1, 1), ("Current CV attached", 0, 1), ("Opt out line", 0, 1)]

def notes(items, kind):
    return "".join(f'<li><b class="{kind}">{n}</b>{t}</li>' for n, t in items)

def col(kind, title, tag, frm, to, subject, body, att, items):
    return f'''<div class="col {kind}"><div class="head"><span class="tag">{tag}</span><h2>{title}</h2></div>
<div class="mail"><div class="f"><span>To</span>{to}</div><div class="f"><span>Subject</span><b>{subject}</b></div>
<div class="body">{body}</div><div class="att"><img src="{icon_uri("pdf")}">{att}</div></div><ul class="notes">{notes(items, kind)}</ul></div>'''

rows = "".join(f'<tr><td>{t}</td><td><img src="{icon_uri("check" if g else "x", "#16a34a" if g else "#dc2626")}"></td><td><img src="{icon_uri("check" if b else "x", "#16a34a" if b else "#dc2626")}"></td></tr>' for t, g, b in SCORE)

html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>
body{{width:1600px;height:900px;background:#f8fafc;padding:48px 56px}}
h1{{font-size:38px;font-weight:800;letter-spacing:-.025em}} .sub{{color:#64748b;font-size:18px;margin-top:6px}}
.grid{{display:grid;grid-template-columns:1fr 1fr 330px;gap:28px;margin-top:30px}}
.head{{display:flex;align-items:center;gap:12px;margin-bottom:14px}} .head h2{{font-size:22px}}
.tag{{font-size:12px;font-weight:800;letter-spacing:.1em;padding:6px 12px;border-radius:99px;color:#fff}}
.bad .tag{{background:#dc2626}} .good .tag{{background:#16a34a}}
.mail{{background:#fff;border-radius:16px;border:1px solid #e2e8f0;box-shadow:0 10px 30px rgba(15,23,42,.06);padding:8px 24px 20px;border-top:6px solid}}
.bad .mail{{border-top-color:#dc2626}} .good .mail{{border-top-color:#16a34a}}
.f{{font-size:14px;padding:10px 0;border-bottom:1px solid #f1f5f9;color:#0f172a}} .f span{{display:inline-block;width:70px;color:#94a3b8}}
.body{{font-size:15px;line-height:1.6;color:#1e293b;margin-top:12px}} .body p{{margin-bottom:10px}}
.hl{{border-radius:4px;padding:1px 2px}} .hl sup{{font-size:10px;font-weight:800;margin-left:2px;color:#fff;border-radius:99px;padding:1px 5px;vertical-align:4px}}
.hl.bad{{background:#fee2e2;text-decoration:underline wavy #f87171 1px;text-underline-offset:3px}} .hl.bad sup{{background:#dc2626}}
.hl.good{{background:#dcfce7}} .hl.good sup{{background:#16a34a}}
.att{{display:inline-flex;gap:8px;align-items:center;font-size:13px;padding:7px 12px;border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc;margin-top:4px}} .att img{{width:20px}}
.bad .att{{border-color:#fca5a5;background:#fef2f2;color:#991b1b}}
.notes{{list-style:none;margin-top:16px}} .notes li{{display:flex;gap:10px;align-items:center;font-size:15px;color:#334155;margin:8px 0}}
.notes b{{width:24px;height:24px;border-radius:50%;color:#fff;display:grid;place-items:center;font-size:12px;flex:none}} .notes b.bad{{background:#dc2626}} .notes b.good{{background:#16a34a}}
.score{{background:#0b1437;border-radius:20px;padding:24px;color:#e2e8f0;align-self:start;margin-top:52px}}
.score h3{{font-size:18px;color:#fff;margin-bottom:14px}} table{{width:100%;border-collapse:collapse;font-size:14px}}
th{{text-align:center;font-size:11px;letter-spacing:.08em;color:#94a3b8;padding-bottom:8px}} th:first-child{{text-align:left}}
td{{padding:9px 0;border-top:1px solid rgba(255,255,255,.1)}} td:not(:first-child){{text-align:center;width:62px}} td img{{width:22px;background:#fff;border-radius:50%;padding:2px}}
.res{{margin-top:16px;font-size:14px;line-height:1.5;color:#cbd5e1}} .res b{{color:#fbbf24}}
</style></head><body>
<h1>Generic vs tailored: the same student, two emails</h1>
<div class="sub">The tool only produces the kind on the right. The claims checker blocks the kind on the left.</div>
<div class="grid">
{col("bad", "Generic", "BEFORE", "", "hr@company.example.com", "Internship application", GENERIC, GENERIC_ATT, GENERIC_NOTES)}
{col("good", "Tailored", "AFTER", "", "Tomas Novak &lt;hello@quill.example.com&gt;", "Internship request · data visualisation", TAILORED, TAILORED_ATT, TAILORED_NOTES)}
<div class="score"><h3>Checklist</h3><table><tr><th></th><th>BEFORE</th><th>AFTER</th></tr>{rows}</table>
<div class="res">A generic email is easy to ignore. A specific, honest one gives the reader <b>a reason to reply</b>.</div></div>
</div></body></html>'''
open("compare.html", "w").write(html)
