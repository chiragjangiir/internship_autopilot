"""Rule based safety net under the assistant's claims check. Run it on every draft before the preview.

usage:  python3 check_draft.py <draft.txt> <facts.md>
        python3 check_draft.py selftest

Errors (exit code 1): over 170 words, no opt out line, generic greeting, a number that is not
in the facts file, or a strong claim phrase that is not in the facts file.
Warnings: unfilled YOUR_ placeholders.
"""
import re, sys

MAX_WORDS = 170
OPT_OUT = re.compile(r"no thanks|not hear from me|unsubscribe|opt out", re.I)
GENERIC = re.compile(r"dear (sir|madam|sir/madam|hiring manager|team)\b|to whom it may concern", re.I)
STRONG = ["led a team", "managed a team", "expert", "world class", "award", "published", "patent",
          "fluent", "increased", "improved", "reduced", "launched", "founded", "top student"]

def check(draft, facts):
    errors, warnings = [], []
    words = len(draft.split())
    if words > MAX_WORDS: errors.append(f"{words} words, limit is {MAX_WORDS}")
    if not OPT_OUT.search(draft): errors.append("no opt out line")
    if GENERIC.search(draft): errors.append("generic greeting, address a named person")
    low_facts = facts.lower()
    for n in sorted(set(re.findall(r"\d+(?:[.,]\d+)?%?", draft))):
        if n not in facts: errors.append(f"number {n} is not in the facts file")
    for p in STRONG:
        if p in draft.lower() and p not in low_facts: errors.append(f"claim \"{p}\" is not in the facts file")
    for ph in sorted(set(re.findall(r"YOUR_[A-Z_]+", draft))): warnings.append(f"placeholder {ph} not filled in")
    return words, errors, warnings

def selftest():
    facts = "Built DATA_VIZ_PROJECT in Python and D3, reworked after user feedback."
    good = "Dear Tomas, I built a dashboard in Python and D3. If you'd rather not hear from me again, reply no thanks."
    bad = "Dear Sir/Madam, I led a team of 10 and improved efficiency by 300%."
    _, e, _ = check(good, facts); assert e == [], e
    _, e, _ = check(bad, facts)
    assert any("generic" in x for x in e) and any("300%" in x for x in e) and any("led a team" in x for x in e) and any("opt out" in x for x in e), e
    _, e, _ = check("word " * 169 + "no thanks", facts); assert any("171 words" in x for x in e), e
    print("selftest passed")

if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]: selftest(); sys.exit(0)
    if len(sys.argv) != 3: sys.exit(__doc__)
    draft, facts = (open(p, encoding="utf8").read() for p in sys.argv[1:])
    words, errors, warnings = check(draft, facts)
    for w in warnings: print("warning:", w)
    for e in errors: print("ERROR:", e)
    print(f"{words} words, {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)
