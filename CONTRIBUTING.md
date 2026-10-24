# Contributing

Issues and pull requests are welcome.

Please do not submit ripped, traced, scraped, or unlicensed artwork from the
original series or other fan projects. Artwork changes must preserve the
transparent background, `1536 × 2288` canvas, `192 × 208` cell geometry, and
the required v2 frame counts.

Before opening a pull request, run:

```bash
python3 -m pip install Pillow
python3 scripts/validate_repo.py
```

Pull requests must keep `manifest.json` and `SHA256SUMS` in sync with changed
assets.
