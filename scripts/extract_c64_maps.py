#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
import json

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "map-sources" / "digital"
OUT_JS = ROOT / "generated" / "c64-generated-maps.js"
OUT_PREVIEW = ROOT / "generated" / "c64-map-preview.html"

MAP_SOURCES = [
    ("N America 1", "01-n-america-1.png"),
    ("Middle East", "02-middle-east.png"),
    ("China", "03-china.png"),
    ("Prussia", "04-prussia.png"),
    ("Mediterranean", "05-mediterranean.png"),
    ("Shenandoah", "06-shenandoah.png"),
    ("N America 2", "07-n-america-2.png"),
    ("European Wars", "08-european-wars.png"),
    ("Africa", "09-africa.png"),
    ("3 Continents", "10-3-continents.png"),
    ("S America", "11-s-america.png"),
    ("Down Under", "12-down-under.png"),
    ("Polar Ice", "13-polar-ice.png"),
    ("World", "14-world.png"),
    ("Early Italia", "15-early-italia.png"),
    ("Caribbean", "16-caribbean.png"),
    ("Sea of Japan", "17-sea-of-japan.png"),
    ("Shenandoah 2", "18-shenandoah-2.png"),
    ("Riverland", "19-riverland.png"),
    ("Borderlands", "20-borderlands.png"),
]


def is_land(px: tuple[int, int, int]) -> bool:
    r, g, b = px
    return g >= 140 and b >= 140 and r <= 170 and abs(g - b) <= 70


def load_land_mask(path: Path, scale: int = 4) -> tuple[list[list[bool]], int, int]:
    img = Image.open(path).convert("RGB")
    w, h = img.size
    sw, sh = w // scale, h // scale
    small = img.resize((sw, sh), Image.Resampling.NEAREST)
    pix = small.load()
    mask = [[False] * sw for _ in range(sh)]
    for y in range(sh):
        for x in range(sw):
            mask[y][x] = is_land(pix[x, y])
    return mask, sw, sh


def components(mask: list[list[bool]], want: bool, min_area: int) -> list[set[tuple[int, int]]]:
    h, w = len(mask), len(mask[0])
    seen = [[False] * w for _ in range(h)]
    out: list[set[tuple[int, int]]] = []
    for y in range(h):
        for x in range(w):
            if seen[y][x] or mask[y][x] != want:
                continue
            q = deque([(x, y)])
            seen[y][x] = True
            cells: set[tuple[int, int]] = set()
            while q:
                cx, cy = q.popleft()
                cells.add((cx, cy))
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and mask[ny][nx] == want:
                        seen[ny][nx] = True
                        q.append((nx, ny))
            if len(cells) >= min_area:
                out.append(cells)
    out.sort(key=lambda c: (min(y for _, y in c), min(x for x, _ in c), -len(c)))
    return out


def dilate(mask: list[list[bool]], radius: int) -> list[list[bool]]:
    h, w = len(mask), len(mask[0])
    out = [[False] * w for _ in range(h)]
    offsets = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if abs(dx) + abs(dy) <= radius:
                offsets.append((dx, dy))
    for y in range(h):
        for x in range(w):
            if not mask[y][x]:
                continue
            for dx, dy in offsets:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    out[ny][nx] = True
    return out


def path_from_cells(cells: set[tuple[int, int]]) -> str:
    edges: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)

    def add(a: tuple[int, int], b: tuple[int, int]) -> None:
        edges[a].append(b)

    for x, y in cells:
        if (x, y - 1) not in cells:
            add((x, y), (x + 1, y))
        if (x + 1, y) not in cells:
            add((x + 1, y), (x + 1, y + 1))
        if (x, y + 1) not in cells:
            add((x + 1, y + 1), (x, y + 1))
        if (x - 1, y) not in cells:
            add((x, y + 1), (x, y))

    parts: list[str] = []
    while edges:
        start = next(iter(edges))
        cur = start
        pts = [start]
        guard = 0
        while guard < 200000:
            guard += 1
            if cur not in edges or not edges[cur]:
                break
            nxt = edges[cur].pop()
            if not edges[cur]:
                del edges[cur]
            pts.append(nxt)
            cur = nxt
            if cur == start:
                break
        if len(pts) > 2:
            bits = [f"M {pts[0][0]} {pts[0][1]}"]
            bits.extend(f"L {x} {y}" for x, y in pts[1:])
            bits.append("Z")
            parts.append(" ".join(bits))
    return " ".join(parts)


def nearby_labels(cells: set[tuple[int, int]], labels: list[list[int]], radius: int) -> set[int]:
    h, w = len(labels), len(labels[0])
    found: set[int] = set()
    offsets = [(dx, dy) for dy in range(-radius, radius + 1) for dx in range(-radius, radius + 1)
               if abs(dx) + abs(dy) <= radius]
    for x, y in cells:
        for dx, dy in offsets:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                lab = labels[ny][nx]
                if lab >= 0:
                    found.add(lab)
    return found


def extract_map(name: str, filename: str) -> dict:
    mask, w, h = load_land_mask(SRC_DIR / filename)
    land_components = components(mask, True, min_area=35)

    land_labels = [[-1] * w for _ in range(h)]
    for i, cells in enumerate(land_components):
        for x, y in cells:
            land_labels[y][x] = i

    water_mask = [[not v for v in row] for row in dilate(mask, radius=2)]
    water_components = components(water_mask, True, min_area=250)
    water_labels = [[-1] * w for _ in range(h)]
    water_offset = len(land_components)
    for i, cells in enumerate(water_components):
        for x, y in cells:
            water_labels[y][x] = water_offset + i

    neighbor_sets = [set() for _ in range(len(land_components) + len(water_components))]

    for i, cells in enumerate(land_components):
        for other in nearby_labels(cells, land_labels, radius=3):
            if other != i:
                neighbor_sets[i].add(other)
        for water in nearby_labels(cells, water_labels, radius=5):
            neighbor_sets[i].add(water)
            neighbor_sets[water].add(i)

    for i, cells in enumerate(water_components):
        idx = water_offset + i
        for other in nearby_labels(cells, water_labels, radius=2):
            if other != idx:
                neighbor_sets[idx].add(other)
                neighbor_sets[other].add(idx)

    territories = []
    for i, cells in enumerate(land_components):
        sx = sum(x + 0.5 for x, _ in cells)
        sy = sum(y + 0.5 for _, y in cells)
        all_neighbors = sorted(neighbor_sets[i])
        territories.append({
            "id": f"{name.lower().replace(' ', '-')}-l{i + 1}",
            "name": f"{name} {i + 1}",
            "d": path_from_cells(cells),
            "cx": round(sx / len(cells), 2),
            "cy": round(sy / len(cells), 2),
            "neighbors": [n for n in all_neighbors if n < water_offset],
            "navalNeighbors": [],
            "allNeighbors": all_neighbors,
        })

    water_set = []
    for i, cells in enumerate(water_components):
        idx = water_offset + i
        sx = sum(x + 0.5 for x, _ in cells)
        sy = sum(y + 0.5 for _, y in cells)
        water_set.append(idx)
        territories.append({
            "id": f"{name.lower().replace(' ', '-')}-w{i + 1}",
            "name": f"{name} Water {i + 1}",
            "d": path_from_cells(cells),
            "cx": round(sx / len(cells), 2),
            "cy": round(sy / len(cells), 2),
            "neighbors": [],
            "navalNeighbors": [],
            "allNeighbors": sorted(neighbor_sets[idx]),
        })

    return {
        "name": name,
        "source": filename,
        "w": w,
        "h": h,
        "territories": territories,
        "waterSet": water_set,
        "landCount": len(land_components),
        "waterCount": len(water_components),
    }


def write_preview(maps: dict[str, dict]) -> None:
    options = "\n".join(f'<option value="{name}">{name}</option>' for name in maps)
    html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>C64 Generated Map Preview</title>
<style>
body{{margin:0;background:#060708;color:#fff;font-family:system-ui,Arial;padding:18px}}
.bar{{display:flex;gap:12px;align-items:center;margin-bottom:14px}}
select{{font:inherit;padding:8px 10px;background:#12151d;color:#fff;border:1px solid #596070;border-radius:8px}}
svg{{width:min(1200px,100%);height:auto;display:block;background:#000;border:1px solid #29313f}}
.land{{fill:#7ff2ef;stroke:#030303;stroke-width:1.2}}
.water{{fill:#020303;stroke:#020303;stroke-width:.35}}
.dot{{fill:#7ff2ef;opacity:.75}}
#stats{{color:#cbd4e4;font-weight:800}}
</style>
</head>
<body>
<div class="bar"><select id="pick">{options}</select><span id="stats"></span></div>
<div id="host"></div>
<script src="c64-generated-maps.js"></script>
<script>
const pick = document.getElementById('pick');
const host = document.getElementById('host');
const stats = document.getElementById('stats');
function render(){{
  const map = window.C64_GENERATED_MAPS[pick.value];
  const waters = new Set(map.waterSet || []);
  stats.textContent = `${{map.landCount}} land territories, ${{map.waterCount}} water regions`;
  host.innerHTML = `<svg viewBox="0 0 ${{map.w}} ${{map.h}}" xmlns="http://www.w3.org/2000/svg"></svg>`;
  const svg = host.firstElementChild;
  map.territories.forEach((t,i)=>{{
    const p = document.createElementNS('http://www.w3.org/2000/svg','path');
    p.setAttribute('d', t.d);
    p.setAttribute('class', waters.has(i) ? 'water' : 'land');
    svg.appendChild(p);
  }});
  for(let y=8;y<map.h;y+=13) for(let x=8;x<map.w;x+=13){{
    const c = document.createElementNS('http://www.w3.org/2000/svg','circle');
    c.setAttribute('cx',x); c.setAttribute('cy',y); c.setAttribute('r',1.2); c.setAttribute('class','dot');
    svg.insertBefore(c, svg.firstChild);
  }}
}}
pick.addEventListener('change', render);
render();
</script>
</body>
</html>
"""
    OUT_PREVIEW.write_text(html)


def main() -> None:
    OUT_JS.parent.mkdir(parents=True, exist_ok=True)
    maps = {name: extract_map(name, filename) for name, filename in MAP_SOURCES}
    payload = json.dumps(maps, separators=(",", ":"))
    names = json.dumps([name for name, _ in MAP_SOURCES])
    OUT_JS.write_text(
        "/* Generated from map-sources/digital by scripts/extract_c64_maps.py. */\n"
        f"window.C64_GENERATED_MAPS={payload};\n"
        f"window.C64_GENERATED_MAP_NAMES={names};\n"
    )
    write_preview(maps)
    for name, data in maps.items():
        print(f"{name}: {data['landCount']} land, {data['waterCount']} water")


if __name__ == "__main__":
    main()
