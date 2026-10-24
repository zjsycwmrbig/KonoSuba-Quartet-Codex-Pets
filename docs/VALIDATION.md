# Validation

Validated on 2026-10-24 against the sprite sheets returned by the Codex Pets
service.

## Official Codex Pets preflight

| Pet | Stable ID | PNG bytes | WebP bytes | Version | Result |
| --- | --- | ---: | ---: | ---: | --- |
| 阿库娅 | `pet_6adad37d859481918b29a99e2d388ccc` | 3,237,702 | 2,565,926 | 2 | `valid: true` |
| 惠惠 | `pet_6adac38a8d28819191f5db9c38f5c71c` | 3,359,714 | 2,634,676 | 2 | `valid: true` |
| Kazuma 和真 | `pet_6ad9e8f1524481919994224aa8b56e8f` | 2,478,208 | 1,768,284 | 2 | `valid: true` |
| 达克妮丝 | `pet_6adaf9cdca788191a52e4d5d03ba4a5a` | 3,288,527 | 2,578,350 | 2 | `valid: true` |

Both the PNG masters and the exact WebP files placed in `pets/<slug>/` passed
the official preflight. All four pairs reported these properties:

- Canvas: `1536 × 2288`
- Cell: `192 × 208`
- Grid: `8 × 11`
- Sprite version: 2
- Frames per row: `6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8`
- Errors: none

## Repository exports

`assets/spritesheets/<slug>.png` contains the exact PNG returned by the Codex
Pets download endpoint and accepted by the official preflight.

`pets/<slug>/spritesheet.webp` is generated losslessly from that PNG and was
separately accepted by the official preflight. The repository validator also
checks that the PNG and WebP decoded pixel buffers match exactly.

File hashes are recorded in [`manifest.json`](../manifest.json) and
[`SHA256SUMS`](../SHA256SUMS).

## Local verification

```bash
python3 -m pip install Pillow
python3 scripts/validate_repo.py
```

The validator also runs in GitHub Actions on every push and pull request.
