"""Generates sequence.svg (+ .html wrapper): detailed, hand-laid-out sequence diagram."""
from html import escape
from icons import icon_uri

LANES = [  # key, title, subtitle, icons
    ("U", "You", "the applicant", ["user_check"]),
    ("A", "Assistant", "AI agent", ["claude"]),
    ("W", "Web search", "public pages", ["search"]),
    ("F", "Project files", "csv · facts · CV", ["microsoft_excel", "markdown"]),
    ("D", "Drafts", "with CV attached", ["folder_open"]),
    ("M", "Mail client", "Apple Mail / Outlook", ["apple_mail", "microsoft_outlook"]),
    ("S", "Sent folder", "delivery proof", ["mail_check"]),
    ("I", "Inbox", "replies", ["inbox"]),
    ("C", "Calendar", "Apple Calendar", ["apple_calendar"]),
]
X0, STEP, W = 120, 176, 1640
LX = {k: X0 + i * STEP for i, (k, *_) in enumerate(LANES)}

# phase, colour, rows. Row kinds: ("msg", from, to, text, dashed) | ("note", lane, [lines]) | ("alt", from, to, title, text)
PHASES = [
    ("1  PREPARE", "#2563eb", [
        ("msg", "U", "A", "Goal: robotics / AI internship, target regions", False),
        ("msg", "A", "W", "Search companies, labs, professors", False),
        ("msg", "W", "A", "Pages + public contact emails + source URLs", True),
        ("note", "A", ["Keep only emails printed on an official page.", "Never guess an address pattern."]),
        ("msg", "A", "F", "Add row to targets.csv (status = new)", False),
        ("msg", "F", "A", "Read facts file + the one current CV", True),
        ("note", "A", ["Write < 170 words: one detail of their work", "+ one matching project from the facts file."]),
        ("note", "A", ["Claims checker: every sentence vs facts file.", "Unsupported or inflated claim → removed."]),
        ("msg", "A", "D", "Create draft, attach current CV (status = drafted)", False),
    ]),
    ("2  APPROVE", "#d97706", [
        ("msg", "A", "U", "Preview: recipient, subject, full body, attachment", False),
        ("msg", "U", "A", "“send”  (or edit / skip)", True),
        ("alt", "U", "D", "if you don’t say “send”", "Draft stays in Drafts. Nothing is sent."),
    ]),
    ("3  SEND & VERIFY", "#7c3aed", [
        ("msg", "A", "F", "Delete old output, then dry run: who would be mailed?", False),
        ("msg", "F", "A", "Dry run list (allow list only)", True),
        ("msg", "A", "M", "Send approved drafts", False),
        ("note", "M", ["Before each mail: on allow list · not in sent_log", "no STOP file · under daily cap · wait 3 to 8 min"]),
        ("msg", "M", "S", "Message delivered", False),
        ("msg", "A", "S", "Poll Sent folder", False),
        ("msg", "S", "A", "Found → verified", True),
        ("msg", "A", "F", "Append sent_log.csv, status = sent", False),
    ]),
    ("4  REPLIES & FOLLOW UP", "#0d9488", [
        ("msg", "I", "A", "Reply arrives", True),
        ("msg", "A", "U", "Full summary + drafted answer", False),
        ("msg", "U", "A", "Approve or edit", True),
        ("msg", "A", "M", "Reply in the same thread", False),
        ("msg", "A", "C", "Add meeting / deadline, alerts 1 d · 1 h · 30 m · 15 m", False),
        ("msg", "A", "F", "Log in status.md, out of office goes to the follow up list", False),
    ]),
]

out = []; add = out.append
tw = lambda s, size=14: len(s) * size * 0.5  # rough text width

def pill(x1, x2, y, text, color="#0f172a", size=14):
    """Label above an arrow; centred if it fits, else starts just after the left lane."""
    w = tw(text, size) + 18
    lo, hi = min(x1, x2), max(x1, x2)
    left = (lo + hi - w) / 2 if w < hi - lo - 30 else lo + 18
    add(f'<rect x="{left:.1f}" y="{y-size-3}" width="{w:.1f}" height="{size+10}" rx="6" fill="#fff" stroke="#e2e8f0"/>')
    add(f'<text x="{left+9:.1f}" y="{y+1}" font-size="{size}" font-weight="500" fill="{color}">{escape(text)}</text>')

HEAD_Y, HEAD_H = 120, 104
y = HEAD_Y + HEAD_H + 40
rows, n = [], 0
for title, color, items in PHASES:
    top = y; y += 50
    for it in items:
        h = {"msg": 64, "note": 72, "alt": 80}[it[0]]
        rows.append((it, y, color)); y += h
    rows.append((("band", title, color), top, y + 10)); y += 34
H = y + 20

body = []
# bands first (behind)
for it, top, bottom in [r for r in rows if r[0][0] == "band"]:
    _, title, color = it
    add(f'<rect x="28" y="{top}" width="{W-56}" height="{bottom-top}" rx="18" fill="{color}" fill-opacity=".06" stroke="{color}" stroke-opacity=".25"/>')
    add(f'<rect x="44" y="{top+12}" width="{tw(title,13)*1.3+36}" height="26" rx="13" fill="{color}"/>')
    add(f'<text x="60" y="{top+30}" font-size="13" font-weight="800" fill="#fff" letter-spacing=".08em">{escape(title)}</text>')
# lifelines
for k, x in LX.items():
    add(f'<line x1="{x}" y1="{HEAD_Y+HEAD_H}" x2="{x}" y2="{H-30}" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 6"/>')
# headers
for k, t, sub, ics in LANES:
    x = LX[k]; fill = "#d97706" if k == "U" else "#0b1437"
    add(f'<rect x="{x-78}" y="{HEAD_Y}" width="156" height="{HEAD_H}" rx="16" fill="{fill}"/>')
    s, gap = 34, 6; x0 = x - (len(ics) * s + (len(ics) - 1) * gap) / 2
    for i, ic in enumerate(ics):
        add(f'<rect x="{x0+i*(s+gap)-4}" y="{HEAD_Y+12}" width="{s+8}" height="{s+8}" rx="10" fill="#fff"/>')
        add(f'<image href="{icon_uri(ic, "#0b1437")}" x="{x0+i*(s+gap)+2}" y="{HEAD_Y+18}" width="{s-4}" height="{s-4}"/>')
    add(f'<text x="{x}" y="{HEAD_Y+75}" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">{escape(t)}</text>')
    add(f'<text x="{x}" y="{HEAD_Y+93}" font-size="11.5" fill="#cbd5e1" text-anchor="middle">{escape(sub)}</text>')
# rows
for it, ry, color in [r for r in rows if r[0][0] != "band"]:
    kind = it[0]
    if kind == "msg":
        n += 1; _, a, b, text, dashed = it; xa, xb = LX[a], LX[b]
        d = 1 if xb > xa else -1; ay = ry + 40
        add(f'<line x1="{xa}" y1="{ay}" x2="{xb - d*2}" y2="{ay}" stroke="{color}" stroke-width="2.2"{" stroke-dasharray=\"7 5\"" if dashed else ""} marker-end="url(#m{color[1:]})"/>')
        add(f'<circle cx="{xa}" cy="{ay}" r="12" fill="{color}"/><text x="{xa}" y="{ay+4.5}" font-size="12" font-weight="800" fill="#fff" text-anchor="middle">{n}</text>')
        pill(xa, xb, ay - 20, text)
    elif kind == "note":
        _, lane, lines = it; x = LX[lane]
        w = max(tw(l, 13.5) for l in lines) + 32
        add(f'<rect x="{x-14}" y="{ry+6}" width="{w}" height="{20*len(lines)+18}" rx="10" fill="#fff" stroke="{color}" stroke-width="1.5"/>')
        add(f'<rect x="{x-8}" y="{ry+14}" width="4" height="{20*len(lines)+2}" rx="2" fill="{color}"/>')
        for i, l in enumerate(lines):
            add(f'<text x="{x+6}" y="{ry+28+i*20}" font-size="13.5" fill="#334155">{escape(l)}</text>')
    elif kind == "alt":
        _, a, b, title, text = it; xa, xb = LX[a] - 50, LX[b] + 70
        add(f'<rect x="{xa}" y="{ry+6}" width="{xb-xa}" height="62" rx="10" fill="#fff" stroke="{color}" stroke-width="1.5" stroke-dasharray="6 5"/>')
        add(f'<rect x="{xa}" y="{ry+6}" width="{tw(title,12.5)+24}" height="24" rx="10" fill="{color}"/>')
        add(f'<text x="{xa+12}" y="{ry+23}" font-size="12.5" font-weight="700" fill="#fff">{escape(title)}</text>')
        add(f'<text x="{xa+14}" y="{ry+54}" font-size="14" fill="#334155">{escape(text)}</text>')

colors = {c for _, c, _ in PHASES}
defs = "".join(f'<marker id="m{c[1:]}" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>' for c in colors)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif">
<defs>{defs}</defs><rect width="{W}" height="{H}" fill="#f8fafc"/>
<text x="40" y="60" font-size="30" font-weight="800" fill="#0f172a" letter-spacing="-.02em">One application, end to end</text>
<text x="40" y="90" font-size="16" fill="#64748b">NTOTAL numbered messages across four phases. Solid arrow = request, dashed = response. Boxes = what happens inside a step.</text>
{chr(10).join(out)}</svg>'''
svg = svg.replace("NTOTAL", str(n))
open("../images/sequence.svg", "w").write(svg)
open("sequence.html", "w").write(f'<!doctype html><meta charset="utf-8"><style>body{{margin:0}}</style>{svg}')
print(W, H)
