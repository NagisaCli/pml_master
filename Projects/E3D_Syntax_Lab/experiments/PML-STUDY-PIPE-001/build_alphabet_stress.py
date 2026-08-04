"""Build an isolated A-Z alphabet from closed DRAWING point loops.

Each occupied 5x7 bitmap cell becomes one closed square DRAWING. Several
DRAWING blocks therefore compose each letter without touching project objects.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[3]
sys.path.insert(0, str(REPO_ROOT))

from wsb.drawing_builder import build_drawing

OUTPUT = ROOT / "candidate" / "drawing_alphabet_a_to_z.pml"
CELL = 100.0
GAP = 25.0
LETTER_GAP = 180.0
ROWS = 5
COLS = 6

PATTERNS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "J": ("00111", "00010", "00010", "00010", "10010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
}


def cell(east: float, north: float) -> str:
    return build_drawing(
        (
            (east, north, 0.0),
            (east + CELL, north, 0.0),
            (east + CELL, north + CELL, 0.0),
            (east, north + CELL, 0.0),
            (east, north, 0.0),
        )
    )


def build() -> str:
    blocks: list[str] = []
    for index, (letter, pattern) in enumerate(PATTERNS.items()):
        grid_row, grid_col = divmod(index, COLS)
        origin_e = grid_col * (5 * (CELL + GAP) + LETTER_GAP)
        origin_n = (ROWS - 1 - grid_row) * (7 * (CELL + GAP) + LETTER_GAP)
        blocks.append(f"-- LETTER {letter}")
        for row, bits in enumerate(pattern):
            for col, bit in enumerate(bits):
                if bit == "1":
                    east = origin_e + col * (CELL + GAP)
                    north = origin_n + (6 - row) * (CELL + GAP)
                    blocks.append(cell(east, north))
    return "\n".join(blocks)


if __name__ == "__main__":
    OUTPUT.write_text(build(), encoding="utf-8", newline="\n")
    print(OUTPUT)
