#!/usr/bin/env python3
"""Download Russ's original images from Cargo into docs/images/.

Run once from this folder:  python3 fetch_images.py
Safe to re-run: files already downloaded are skipped.
"""
import json, os, sys, time, urllib.request

here = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(here, 'images.json')))
ok = skipped = 0
failed = []
for i, it in enumerate(items, 1):
    out = 'docs' if os.path.isdir(os.path.join(here, 'docs')) or not os.path.isdir(os.path.join(here, 'public')) else 'public'
    dest = os.path.join(here, out, it['path'])
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        skipped += 1
        continue
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        req = urllib.request.Request(it['url'], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, 'wb') as f:
            f.write(r.read())
        ok += 1
        print(f'[{i}/{len(items)}] {it["path"]}')
        time.sleep(0.2)
    except Exception as e:
        failed.append((it['url'], str(e)))
        print(f'[{i}/{len(items)}] FAILED {it["url"]}: {e}', file=sys.stderr)
print(f'\nDownloaded {ok}, already had {skipped}, failed {len(failed)}.')
if failed:
    print('Failed files are listed above. Re-run to retry, or save them from the Cargo page by hand.')
