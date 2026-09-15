# -*- coding: utf-8 -*-
import json
import math

with open('Projects/scratch_cad_column.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prims = data['groups'][0]['primitives']
print(f"Total primitives: {len(prims)}")

# Print all lines
for i, p in enumerate(prims):
    x1, y1 = p['start']['x'], p['start']['y']
    x2, y2 = p['end']['x'], p['end']['y']
    h = p['handle']
    print(f"[{i:2d}] Handle {h:6s}: ({x1:9.4f}, {y1:9.4f}) -> ({x2:9.4f}, {y2:9.4f})")

# Let us find all bounding stations along X
xs = sorted(list(set([p['start']['x'] for p in prims] + [p['end']['x'] for p in prims])), reverse=True)
print("\nStations (X from East to West):")
for i in range(len(xs) - 1):
    x_east = xs[i]
    x_west = xs[i+1]
    dx = x_east - x_west
    print(f"\nSegment {i+1}: X in [{x_west:.4f}, {x_east:.4f}] (Length = {dx:.4f})")
    # Find lines in this segment
    seg_lines = []
    for p in prims:
        px_min = min(p['start']['x'], p['end']['x'])
        px_max = max(p['start']['x'], p['end']['x'])
        if px_min <= x_west + 1e-3 and px_max >= x_east - 1e-3:
            seg_lines.append(p)
        elif abs(px_min - px_max) < 1e-3 and (abs(px_min - x_east) < 1e-3 or abs(px_min - x_west) < 1e-3):
            # Vertical boundary line
            pass
    for sl in seg_lines:
        print(f"  Crossing Line {sl['handle']}: ({sl['start']['x']:.2f}, {sl['start']['y']:.2f}) -> ({sl['end']['x']:.2f}, {sl['end']['y']:.2f})")
