# Russ Gottwald portfolio

A plain static site, published with GitHub Pages at www.russgottwald.com.

## Contents
- `settings.py` holds email, LinkedIn, location and the site address. Updates to `build.py` never overwrite it.
- `build.py` holds the content (projects, resume, about) and generates the site into `docs/`.
- `docs/` is the website. GitHub Pages publishes this folder.
- `fetch_images.py` downloads Russ's original images from Cargo into `docs/images/`.
- `images.json` lists those images; `build.py` writes it.
- `src/` holds the stylesheet, the T animation and the small site script.

## Work grid
- `WORK_ORDER` in `build.py` sets the order of the Work page. Projects left out of it still get a page but aren't in the grid.
- New projects waiting on material are marked `draft=True`. Set `SHOW_DRAFTS = True` in `settings.py` to preview them.
- For a new project, put its images in `docs/images/<slug>/`, fill in its entry, and remove `draft=True`.
- `PORTRAIT` in `settings.py` picks the About headshot: `russ-4604.jpg` or `russ-conventional.jpg`.

## Every update
1. Edit `settings.py` or the CONTENT section of `build.py`.
2. Run `python3 build.py` (on Windows, `py build.py`).
3. In GitHub Desktop: write a short summary, click **Commit to main**, then **Push origin**. The live site updates in about a minute.

## Coming from the earlier Netlify version
Copy your settings into `settings.py`, then run `python3 build.py`. It renames your old `public` folder to `docs` and keeps the images you already downloaded.
