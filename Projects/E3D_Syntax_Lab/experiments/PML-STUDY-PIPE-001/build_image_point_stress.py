"""Convert a public-domain SVG line drawing into isolated E3D DRAWING blocks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[3]
sys.path.insert(0, str(REPO_ROOT))

from wsb.drawing_builder import build_drawing

SOURCE = ROOT / "source" / "kiss-line_drawing.svg"
OUTPUT = ROOT / "candidate" / "drawing_image_kiss_high_precision.pml"
TOKEN = re.compile(r"[A-Za-z]|[-+]?(?:\d+\.?\d*|\.\d+)")


def cubic(a, b, c, d, t):
    u = 1.0 - t
    return (
        u**3 * a[0] + 3 * u * u * t * b[0] + 3 * u * t * t * c[0] + t**3 * d[0],
        u**3 * a[1] + 3 * u * u * t * b[1] + 3 * u * t * t * c[1] + t**3 * d[1],
    )


def parse_path(path: str, samples_per_curve: int = 80):
    tokens = TOKEN.findall(path)
    index = 0
    command = None
    current = (0.0, 0.0)
    start = current
    points: list[tuple[float, float]] = []
    while index < len(tokens):
        if tokens[index].isalpha():
            command = tokens[index]
            index += 1
            if command.lower() == "z":
                if points and points[-1] != start:
                    points.append(start)
                current = start
                command = None
                continue
        if command is None:
            raise ValueError("SVG path has coordinates without a command")
        relative = command.islower()
        op = command.upper()
        if op == "M":
            x, y = map(float, tokens[index:index + 2])
            index += 2
            if relative:
                x += current[0]; y += current[1]
            current = (x, y)
            start = current
            points.append(current)
            command = "l" if relative else "L"
        elif op == "C":
            values = list(map(float, tokens[index:index + 6]))
            index += 6
            base = current
            controls = [(values[0], values[1]), (values[2], values[3]), (values[4], values[5])]
            if relative:
                controls = [(base[0] + x, base[1] + y) for x, y in controls]
            for step in range(1, samples_per_curve + 1):
                points.append(cubic(base, controls[0], controls[1], controls[2], step / samples_per_curve))
            current = controls[2]
        else:
            raise ValueError(f"Unsupported SVG path command {command!r}")
    if points and points[-1] != start:
        points.append(start)
    return points


def build() -> str:
    import xml.etree.ElementTree as ET

    root = ET.parse(SOURCE).getroot()
    viewbox = tuple(map(float, root.attrib["viewBox"].split()))
    _, _, width, height = viewbox
    blocks = []
    for element in root.iter():
        if element.tag.endswith("path") and element.attrib.get("d"):
            contour = parse_path(element.attrib["d"])
            # Scale to a practical E3D drawing envelope and invert image Y.
            points = tuple((x * 10.0, (height - y) * 10.0, 0.0) for x, y in contour)
            blocks.append(build_drawing(points))
    return "\n".join(blocks)


if __name__ == "__main__":
    OUTPUT.write_text(build(), encoding="utf-8", newline="\n")
    print(OUTPUT)
