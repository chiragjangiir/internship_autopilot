"""Lists visible text in every rendered page that contains a hyphen, dash or semicolon.
usage: python3 check_text.py   (exit code 1 if anything is found)"""
import pathlib, subprocess, sys, os
from html.parser import HTMLParser

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
BANNED = "-–—;"

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.out = []
    def handle_starttag(self, t, a): self.skip += t in ("style", "script")
    def handle_endtag(self, t): self.skip -= t in ("style", "script")
    def handle_data(self, d):
        if not self.skip and d.strip(): self.out.append(d.strip())

bad = 0
for page in sorted(pathlib.Path(__file__).parent.glob("*.html")):
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=4000", "--dump-dom", page.resolve().as_uri()],
                         capture_output=True, text=True).stdout
    p = Text(); p.feed(dom)
    for line in p.out:
        if any(c in line for c in BANNED):
            bad += 1; print(f"{page.name}: {line}")
sys.exit(1 if bad else 0)
