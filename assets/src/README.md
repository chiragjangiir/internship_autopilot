# Image sources

Every image in `assets/images/` is rendered from the files in this folder. Edit the source, then rebuild everything:

```bash
assets/src/build.sh
```

The build needs Google Chrome (used headless) and Python 3 with Pillow. It ends with `check_text.py`, which fails if any visible text contains a hyphen, a dash or a semicolon.

<table>
<tr><th>Image</th><th>Source</th></tr>
<tr><td>hero.png</td><td>hero.html with AI background art in hero_bg.png</td></tr>
<tr><td>architecture.png and .svg</td><td>architecture.py</td></tr>
<tr><td>workflow.png</td><td>workflow.py</td></tr>
<tr><td>workflow.gif</td><td>gif.py (same steps as workflow.py)</td></tr>
<tr><td>sequence.png and .svg</td><td>sequence.py</td></tr>
<tr><td>safety.png</td><td>safety.py</td></tr>
<tr><td>mock_*.png</td><td>mockups.py (fictional data only)</td></tr>
<tr><td>compare.png</td><td>compare.py</td></tr>
<tr><td>setup.png, faq.png</td><td>panels.py</td></tr>
</table>

## Credits

* Hero background art: generated with an AI image model in Figma, with no text in the image.
* Line icons: [Lucide](https://lucide.dev), ISC license.
* App logos: from the open icon sets on [Iconify](https://iconify.design). Apple Mail and Apple Calendar icons were exported from the apps. All logos are trademarks of their owners and are used only to show compatibility.
