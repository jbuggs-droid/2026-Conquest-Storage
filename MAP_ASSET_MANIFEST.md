# C64 Map Name Manifest

Initial photo references were ingested from `/Users/julianbuggs/Downloads/drive-download-20260428T154408Z-3-001/` on 2026-04-28, then removed from the workspace after Julian requested that the names be kept and the rough photo assets deleted.

Clean digital map screenshots were ingested from `/Users/julianbuggs/Documents/` on 2026-04-28. The timestamp order maps to the original C64 list order below.

## Map Names

| Slot | Map Name |
| ---: | --- |
| 1 | N America 1 |
| 2 | Middle East |
| 3 | China |
| 4 | Prussia |
| 5 | Mediterranean |
| 6 | Shenandoah |
| 7 | N America 2 |
| 8 | European Wars |
| 9 | Africa |
| 10 | 3 Continents |
| 11 | S America |
| 12 | Down Under |
| 13 | Polar Ice |
| 14 | World |
| 15 | Early Italia |
| 16 | Caribbean |
| 17 | Sea of Japan |
| 18 | Shenandoah 2 |
| 19 | Riverland |
| 20 | Borderlands |

## Implementation Decisions

- Use the digital map source as the reference for playable map geometry.
- Generate new thumbnails from the generated/playable maps for use in the setup menu.
- Keep the original C64 map names in the selector.
- Show a map in the setup selector only after playable geometry is ready.

## Playable Geometry Status

- Generated playable geometry exists for all 20 C64 maps in `generated/c64-generated-maps.js`.
- The extraction script is `scripts/extract_c64_maps.py`.
- A standalone preview is available at `generated/c64-map-preview.html`.
- `LoC-ultimate-rev1.html` now loads generated C64 maps and lists the 20 C64 names in the setup map selector.
- Setup menu thumbnail rendering is still pending; generated geometry should be the source for those thumbnails.
