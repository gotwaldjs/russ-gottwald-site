# Russ Gottwald portfolio

A plain static site: no framework and nothing to install beyond Python 3.

## Contents
- `public/` is the website. Upload this folder to the host.
- `build.py` holds all the content (projects, resume, about, email, LinkedIn) and regenerates `public/`.
- `fetch_images.py` downloads Russ's original images from Cargo into `public/images/`.
- `images.json` lists those 264 images. `build.py` writes it, and `fetch_images.py` reads it.
- `src/` holds the stylesheet, the T animation, and the small filter script.

## Go live
1. Run `python3 fetch_images.py` from this folder. This has to happen before Cargo is retired, because the images come from there.
2. Open `public/index.html` in a browser and click through the pages.
3. Edit `EMAIL`, `LINKEDIN` and `LOCATION` at the top of `build.py`, then run `python3 build.py`.
4. Deploy `public/` to a static host, such as Netlify (drag-and-drop deploy), Cloudflare Pages or GitHub Pages. All three have free tiers.
5. Optional: buy a domain, point it at the host, and put that address in `SITE_URL`. Then rebuild so link previews show images.
6. After that, the Cargo site gets pointed at the new address.

## Editing
Change anything in the CONTENT section of `build.py`, then run `python3 build.py`.
- Text in [brackets] is a placeholder. Fill it in, or set `SHOW_PROMPTS = False` to hide the unfilled prompts.
- A media item is either an image filename or `vimeo:ID`. A section with more than six images becomes a sideways-scrolling deck.
- For new images, put the files in `public/images/<project-slug>/` and list their filenames in that project's section.
