# Contributing

Thanks for helping. Small, focused changes are the easiest to review.

## Ground rules

* **No real personal data.** Use fictional names and addresses ending in `example.com`. Run `python3 scripts/check_private.py` before you open a pull request.
* **Keep the guard rails.** Changes that remove approval, the allow list, the sent log, the daily cap, the pauses or the STOP switch will not be merged.
* **No mass mailing features.** Bulk lists, tracking pixels or address guessing are out of scope.

## Before you open a pull request

```bash
python3 scripts/check_draft.py selftest
python3 scripts/check_private.py selftest
python3 scripts/check_private.py
```

If you changed an image, edit its source in `assets/src/` and run `assets/src/build.sh`. Never edit the PNG files directly.

## Writing style

Short sentences, plain words. Prose in this repository uses no hyphens, dashes or semicolons, and the image build checks this automatically.
