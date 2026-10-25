# Example data

Everything in this folder is **fictional**. People, organisations and addresses are made up, and every address ends in `example.com`, a domain reserved for examples. The files match the screenshots in the main README.

Try the checkers on it:

```bash
python3 scripts/check_draft.py examples/draft_quill.txt examples/facts.md
python3 scripts/check_draft.py examples/draft_generic.txt examples/facts.md
```

The first one passes. The second one fails on four rules: no opt out line, a generic greeting, a number that is not in the facts file and an inflated claim.
