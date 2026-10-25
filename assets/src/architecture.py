"""Generates architecture.svg (and an .html wrapper for PNG rendering)."""
from html import escape
import base64, pathlib

def icon_uri(name, color="#0f172a"):
    p = next(pathlib.Path("icons").glob(name + ".*"))
    data = p.read_bytes()
    if p.suffix == ".svg":
        data = data.replace(b"currentColor", color.encode())
        return "data:image/svg+xml;base64," + base64.b64encode(data).decode()
    return "data:image/png;base64," + base64.b64encode(data).decode()

def icons_at(x, y, names, color, size=44):
    for i, n in enumerate(names):
        ix = x + i * (size - 10)
        add(f'<rect x="{ix-4}" y="{y-4}" width="{size+8}" height="{size+8}" rx="14" fill="#fff" stroke="{color}" stroke-opacity=".25"/>')
        add(f'<image href="{icon_uri(n, color)}" x="{ix+4}" y="{y+4}" width="{size-8}" height="{size-8}"/>')
    return x + len(names) * (size - 10) + 10 + 14

W, H = 1600, 1110
out = []
add = out.append

def card(x, y, w, h, icon, title, lines=(), color="#2563eb", chips=()):
    add(f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#fff" stroke="{color}" stroke-opacity=".35" stroke-width="1.5"/></g>')
    add(f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="4" fill="{color}"/>')
    tx = icons_at(x + 20, y + 24, icon if isinstance(icon, list) else [icon], color)
    add(f'<text x="{tx}" y="{y+43}" font-size="17" font-weight="700" fill="#0f172a">{escape(title)}</text>')
    for i, l in enumerate(lines):
        add(f'<text x="{tx}" y="{y+66+i*20}" font-size="13.5" fill="#475569">{escape(l)}</text>')
    cx, cy = x + 20, y + h - 40
    for c in chips:
        cw = 14 + len(c) * 7.4
        if cx + cw > x + w - 14:
            cx, cy = x + 20, cy - 34
        add(f'<rect x="{cx}" y="{cy}" width="{cw}" height="24" rx="12" fill="{color}" fill-opacity=".09"/>')
        add(f'<text x="{cx+cw/2}" y="{cy+16.5}" font-size="12.5" text-anchor="middle" fill="{color}" font-family="ui-monospace,Menlo,monospace">{escape(c)}</text>')
        cx += cw + 8

def band(y, h, num, label, tint):
    add(f'<rect x="30" y="{y}" width="{W-60}" height="{h}" rx="24" fill="{tint}" fill-opacity=".07" stroke="{tint}" stroke-opacity=".25" stroke-dasharray="6 6"/>')
    add(f'<rect x="54" y="{y-14}" width="{48+len(label)*10}" height="28" rx="14" fill="{tint}"/>')
    add(f'<text x="68" y="{y+5}" font-size="13" font-weight="800" fill="#fff" letter-spacing=".08em">{num}  {escape(label)}</text>')

def arrow(d, color="#64748b", dash=False, label=None, lx=0, ly=0):
    da = ' stroke-dasharray="7 6"' if dash else ''
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5"{da} marker-end="url(#a{color[1:]})"/>')
    if label:
        add(f'<rect x="{lx-len(label)*3.6-10}" y="{ly-15}" width="{len(label)*7.2+20}" height="24" rx="12" fill="#fff" stroke="{color}" stroke-opacity=".4"/>')
        add(f'<text x="{lx}" y="{ly+2}" font-size="12.5" text-anchor="middle" fill="{color}" font-weight="600">{escape(label)}</text>')

C = dict(blue="#2563eb", teal="#0d9488", violet="#7c3aed", amber="#d97706", rose="#e11d48", green="#16a34a", slate="#64748b", sky="#0284c7")

# bands
band(120, 330, "1", "PREPARE", C["blue"])
band(495, 150, "2", "APPROVE", C["amber"])
band(690, 210, "3", "SEND", C["violet"])
band(945, 140, "4", "FOLLOW UP", C["teal"])

# 1 prepare
X = [70, 368, 666, 964, 1262]; CW = 266
card(X[0], 160, CW, 150, "claude", "Research agent", ["Finds companies, labs,", "professors + public email"], C["blue"], ["never guesses emails"])
card(X[1], 160, CW, 150, "microsoft_excel", "targets.csv", ["org · person · email ·", "source · why it fits"], C["sky"], ["allow list"])
card(X[2], 160, CW, 150, "claude_code", "CV + email writer", ["Master CV, one email", "per person, < 170 words"], C["violet"], ["1 detail · 1 project"])
card(X[3], 160, CW, 150, "shield_check", "Claims checker", ["Every sentence must", "match the facts file"], C["rose"], ["no exaggeration"])
card(X[4], 160, CW, 150, ["apple_mail","microsoft_outlook"], "Drafts", ["CV attached.", "Nothing sent yet."], C["slate"], ["Mail", "Outlook"])
card(X[2], 345, X[3]+CW-X[2], 85, ["markdown","pdf"], "Facts file  +  current CV", ["The single source of truth. Old CVs are archived."], C["green"])
for i in range(4):
    arrow(f"M{X[i]+CW} 235 H{X[i+1]-8}", C["blue"])
arrow(f"M{X[2]+CW//2} 345 V318", C["green"]); arrow(f"M{X[3]+CW//2} 345 V318", C["green"])

# 2 approve
card(1170, 520, 360, 105, "eye", "Preview every email", ["Full text, recipient, attachment"], C["amber"])
add('<g filter="url(#sh)"><rect x="700" y="520" width="390" height="105" rx="52" fill="#fef3c7" stroke="#d97706" stroke-width="3"/></g>')
icons_at(730, 546, ['user_check'], '#d97706')
add('<text x="815" y="565" font-size="20" font-weight="800" fill="#92400e">You type “send”</text>')
add('<text x="815" y="590" font-size="13.5" fill="#92400e">No approval → nothing leaves the outbox</text>')
arrow(f"M{X[4]+CW//2} 310 V512", C["slate"]); arrow("M1170 572 H1098", C["amber"])

# 3 send
card(70, 730, 560, 150, ["apple","apple_mail"], "Mac · Apple Mail (AppleScript)", ["Picks the sender account, attaches the CV,", "then polls the Sent folder to verify delivery"], C["violet"], ["send_att.sh", "reply_in_thread.sh", "Sent check ✔"])
card(670, 730, 560, 150, ["microsoft_windows","microsoft_outlook","powershell"], "Windows PC · Outlook (COM)", ["Sends only listed drafts, 24/7 via scheduled", "task on a spare PC, reached over SSH/VPN"], C["blue"], ["send_drafts.ps1", "only list", "cap/day", "3 to 8 min", "dry run", "STOP"])
card(1270, 730, 260, 150, "microsoft_excel", "sent_log.csv", ["Every address once.", "Checked before each send"], C["slate"], ["no double mail"])
arrow("M840 625 C 840 680, 350 670, 350 722", C["amber"], label="approved", lx=560, ly=665)
arrow("M950 625 V722", C["amber"])
arrow("M1230 805 H1262", C["slate"])

# 4 follow up
card(70, 970, 270, 100, ["apple_mail","microsoft_outlook"], "Replies", ["Read in full"], C["teal"])
card(380, 970, 290, 100, "claude", "Summary + draft answer", ["Waits for your approval"], C["teal"])
card(710, 970, 250, 100, "list_checks", "follow up list", ["Out of office, redirects"], C["sky"])
card(1000, 970, 270, 100, "apple_calendar", "Apple Calendar", ["Alerts 1d · 1h · 30m · 15m"], C["rose"])
card(1310, 970, 220, 100, "markdown", "status.md", ["Meetings + decisions"], C["green"])
arrow("M200 880 V962", C["teal"]); arrow("M340 1020 H372", C["teal"]); arrow("M670 1020 H702", C["teal"])
arrow("M960 1020 H992", C["teal"]); arrow("M1270 1020 H1302", C["teal"])
arrow("M525 970 V922 H14 V572 H692", C["amber"], dash=True, label="replies go back through approval", lx=330, ly=572)

defs = "".join(f'<marker id="a{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>' for c in C.values())
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif">
<defs>{defs}<filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0f172a" flood-opacity=".08"/></filter>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f8fafc"/><stop offset="1" stop-color="#eef2ff"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<text x="40" y="62" font-size="30" font-weight="800" fill="#0f172a" letter-spacing="-.02em">How Internship Application Autopilot works</text>
<text x="40" y="92" font-size="16" fill="#64748b">From web research to a verified send: the assistant prepares, you approve, a mail client sends, replies loop back.</text>
{chr(10).join(out)}
</svg>'''
open("../images/architecture.svg", "w").write(svg)
open("architecture.html", "w").write(f'<!doctype html><meta charset="utf-8"><style>body{{margin:0}}</style>{svg}')
