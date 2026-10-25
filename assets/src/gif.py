"""Renders workflow.gif: one frame per workflow step, then a summary frame."""
import os, pathlib, subprocess, tempfile
from icons import icon_uri
from workflow import steps  # same texts as workflow.png

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
W, H = 1200, 530
here = pathlib.Path(__file__).parent

def frame(active):
    dots = "".join(f'<div class="d {"on" if i == active else "done" if i < active else ""}" style="--c:{c}">'
                   f'<img src="{icon_uri(ics[0], "#fff" if i == active else c)}"></div>'
                   for i, (_, _, ics, c) in enumerate(steps))
    if active < len(steps):
        t, d, ics, c = steps[active]
        imgs = "".join(f'<span><img src="{icon_uri(n, c)}"></span>' for n in ics)
        main = f'<div class="card" style="--c:{c}"><div class="num">{active + 1}</div><div class="ics">{imgs}</div><h2>{t}</h2><p>{d}</p></div>'
    else:
        main = f'<div class="card" style="--c:#16a34a"><div class="ics"><span><img src="{icon_uri("mail_check", "#16a34a")}"></span></div><h2>Interview booked</h2><p>Eight steps, one human decision. Nothing was sent without your “send”.</p></div>'
    pct = min(active + 1, len(steps)) / len(steps) * 100
    bar_c = steps[active][3] if active < len(steps) else "#16a34a"
    label = f"step {active + 1} of {len(steps)}" if active < len(steps) else "done"
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{(here / "base.css").as_uri()}"><style>
body{{width:{W}px;height:{H}px;background:#f8fafc;padding:40px 56px;overflow:hidden}}
.top{{display:flex;justify-content:space-between;align-items:center}} .top b{{font-size:22px;letter-spacing:-.01em}} .top span{{color:#64748b;font-size:16px}}
.bar{{height:8px;border-radius:4px;background:#e2e8f0;margin:18px 0 26px}} .bar i{{display:block;height:100%;width:{pct}%;border-radius:4px;background:{bar_c}}}
.dots{{display:flex;justify-content:space-between}} .d{{width:62px;height:62px;border-radius:18px;background:#fff;border:2px solid #e2e8f0;display:grid;place-items:center;opacity:.55}}
.d img{{width:30px;height:30px}} .d.done{{opacity:1;border-color:var(--c)}} .d.on{{opacity:1;background:var(--c);border-color:var(--c);transform:scale(1.15);box-shadow:0 8px 20px rgba(15,23,42,.2)}}
.card{{margin-top:34px;background:#fff;border-radius:24px;padding:30px 36px;border:1px solid #e2e8f0;border-top:8px solid var(--c);box-shadow:0 14px 40px rgba(15,23,42,.08);position:relative;min-height:270px}}
.num{{position:absolute;right:36px;top:26px;width:64px;height:64px;border-radius:50%;background:var(--c);color:#fff;font-size:32px;font-weight:800;display:grid;place-items:center}}
.ics{{display:flex;gap:10px}} .ics span{{width:64px;height:64px;border-radius:18px;border:1px solid #e2e8f0;display:grid;place-items:center}} .ics img{{width:42px;height:42px}}
h2{{font-size:34px;letter-spacing:-.02em;margin:20px 0 10px}} p{{font-size:21px;line-height:1.5;color:#475569;max-width:900px}}
</style></head><body><div class="top"><b>Internship Application Autopilot</b><span>{label}</span></div>
<div class="bar"><i></i></div><div class="dots">{dots}</div>{main}</body></html>'''

with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)
    for i in range(len(steps) + 1):
        (tmp / f"f{i}.html").write_text(frame(i))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                        f"--screenshot={tmp / f'f{i:02d}.png'}", (tmp / f"f{i}.html").as_uri()], capture_output=True, check=True)
    # Pillow only (no ffmpeg needed): clean cuts, 1.8 s per step, 3.5 s on the last frame
    from PIL import Image
    shots = [Image.open(tmp / f"f{i:02d}.png").convert("RGB") for i in range(len(steps) + 1)]
    frames, durations = [], []
    for i, im in enumerate(shots):
        frames.append(im); durations.append(3500 if i == len(shots) - 1 else 1800)
    # one shared palette taken from all frames, so colours never shift between frames
    strip = Image.new("RGB", (W, H * len(frames)))
    for i, f in enumerate(frames): strip.paste(f, (0, i * H))
    palette = strip.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    pal = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    out = here.parent / "images" / "workflow.gif"
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True)
    print(out.name, round(out.stat().st_size / 1e6, 2), "MB")
