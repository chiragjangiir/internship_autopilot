"""Scans the repository for personal data before you publish it.

usage:  python3 check_private.py [folder]        (default: the repository root)
        python3 check_private.py selftest

Finds: email addresses outside example.com, phone numbers, IBANs, IP addresses, Tailscale names,
API keys and tokens. Add your own name, school, city and usernames, one per line, to
private_words.txt in the repository root. That file is in .gitignore, so it never gets published.
"""
import pathlib, re, sys

PATTERNS = {
    "email": re.compile(r"[\w.+]+@(?![\w.]*example\.(com|org)\b)[\w]+(\.[\w]+)+"),
    "phone": re.compile(r"\+\d[\d ()]{8,}\d"),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,7}\b"),
    "ip address": re.compile(r"\b(?!127\.0\.0\.1\b)(?!0\.0\.0\.0\b)(?:\d{1,3}\.){3}\d{1,3}\b"),
    "tailscale name": re.compile(r"\.ts\.net\b|\btailnet\b", re.I),
    "api key or token": re.compile(r"\b(sk_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bp]-[A-Za-z0-9-]{10,})"),
}
TEXT = {".md", ".txt", ".csv", ".py", ".sh", ".ps1", ".html", ".svg", ".css", ".json", ".yml", ".gitignore", ""}

def scan_text(text, words):
    hits = []
    for name, rx in PATTERNS.items():
        hits += [(name, m.group(0)) for m in rx.finditer(text)]
    low = text.lower()
    hits += [("private word", w) for w in words if w in low]
    return hits

def scan(root):
    root = pathlib.Path(root)
    pw = root / "private_words.txt"
    words = [w.strip().lower() for w in pw.read_text().splitlines() if w.strip()] if pw.exists() else []
    found = 0
    for f in sorted(root.rglob("*")):
        if not f.is_file() or ".git" in f.parts or f.name in ("private_words.txt", "check_private.py") or f.suffix.lower() not in TEXT:
            continue
        text = re.sub(r"data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+", "", f.read_text(errors="ignore"))  # skip embedded icons
        for name, value in scan_text(text, words):
            found += 1; print(f"{f.relative_to(root)}: {name}: {value}")
    print(f"{found} findings" + ("" if words else " (no private_words.txt, so names were not checked)"))
    return found

def selftest():
    sample = "mail me at real.person@mailbox.org or demo@example.com, call +1 555 010 0199, IBAN GB82 WEST 1234 5698 7654 32, host 192.0.2.7, box.tail1234.ts.net"
    kinds = {k for k, _ in scan_text(sample, ["exampleschool"])}
    assert kinds == {"email", "phone", "iban", "ip address", "tailscale name"}, kinds
    assert not scan_text("demo@example.com and a.rivera@northwind.example.com", []), "example.com must pass"
    assert scan_text("I studied at ExampleSchool", ["exampleschool"]) == [("private word", "exampleschool")]
    print("selftest passed")

if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]: selftest(); sys.exit(0)
    sys.exit(1 if scan(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent) else 0)
