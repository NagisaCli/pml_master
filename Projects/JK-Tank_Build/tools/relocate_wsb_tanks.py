"""
Relocate all equipment in WSB_TA by (E 51267mm, N 58841mm, U 0mm).
Preserves all internal primitives, nozzles, and structural paths byte-for-byte.
"""

from __future__ import annotations

import difflib
import hashlib
from pathlib import Path
import re

import sys

repo_root = Path(__file__).resolve().parents[2]  # c:\Muvsera\Projects\e3d_agent if in tools
if not (repo_root / "wsb").exists():
    repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from wsb.pml_builder import validate_pml

DE = 51267.0
DN = 58841.0
DU = 0.0

def parse_pos(pos_str: str) -> tuple[float, float, float]:
    tokens = pos_str.strip().split()
    e, n, u = 0.0, 0.0, 0.0
    i = 0
    while i < len(tokens):
        axis = tokens[i].upper()
        val = float(tokens[i+1].lower().replace("mm", ""))
        if axis == "E":
            e = val
        elif axis == "W":
            e = -val
        elif axis == "N":
            n = val
        elif axis == "S":
            n = -val
        elif axis == "U":
            u = val
        elif axis == "D":
            u = -val
        i += 2
    return e, n, u


def format_pos(e: float, n: float, u: float) -> str:
    def fmt_val(v: float) -> str:
        r = round(v, 2)
        if abs(r - round(r)) < 1e-5:
            return f"{int(round(r))}mm"
        return f"{r:.2f}".rstrip("0").rstrip(".") + "mm"

    e_str = f"E {fmt_val(e)}" if e >= 0 else f"W {fmt_val(-e)}"
    n_str = f"N {fmt_val(n)}" if n >= 0 else f"S {fmt_val(-n)}"
    u_str = f"U {fmt_val(u)}" if u >= 0 else f"D {fmt_val(-u)}"
    return f"POS {e_str} {n_str} {u_str}"


def transform(source_lines: list[str]) -> tuple[list[str], list[dict]]:
    new_lines: list[str] = []
    i = 0
    records: list[dict] = []

    while i < len(source_lines):
        line = source_lines[i]
        m_eq = re.match(r"^NEW\s+EQUIPMENT\s+(/\S+)", line.strip(), re.IGNORECASE)
        m_stru = re.match(r"^NEW\s+STRUCTURE\s+(/\S+)", line.strip(), re.IGNORECASE)

        if m_eq:
            eq_name = m_eq.group(1)
            new_lines.append(line)
            i += 1
            header_lines: list[str] = []
            pos_found = False

            while i < len(source_lines):
                l_strip = source_lines[i].strip()
                if (
                    l_strip.startswith("NEW SUBEQUIPMENT")
                    or l_strip.startswith("NEW EQUIPMENT")
                    or l_strip.startswith("NEW STRUCTURE")
                    or l_strip == "END"
                ):
                    break
                m_pos = re.match(r"^POS\s+(.+)", l_strip, re.IGNORECASE)
                if m_pos:
                    pos_found = True
                    orig_pos_str = m_pos.group(1)
                    e, n, u = parse_pos(orig_pos_str)
                    new_pos_str = format_pos(e + DE, n + DN, u + DU)
                    header_lines.append(new_pos_str)
                    records.append({
                        "type": "EQUIPMENT",
                        "name": eq_name,
                        "old_pos": orig_pos_str,
                        "new_pos": new_pos_str,
                        "e_new": e + DE,
                        "n_new": n + DN,
                        "u_new": u + DU,
                    })
                else:
                    header_lines.append(source_lines[i])
                i += 1

            if not pos_found:
                new_pos_str = format_pos(DE, DN, DU)
                func_idx = -1
                for idx, hl in enumerate(header_lines):
                    if hl.strip().startswith("FUNC"):
                        func_idx = idx
                        break
                if func_idx != -1:
                    header_lines.insert(func_idx + 1, new_pos_str)
                else:
                    header_lines.insert(0, new_pos_str)
                records.append({
                    "type": "EQUIPMENT",
                    "name": eq_name,
                    "old_pos": "None (0,0,0)",
                    "new_pos": new_pos_str,
                    "e_new": DE,
                    "n_new": DN,
                    "u_new": DU,
                })

            new_lines.extend(header_lines)
            continue

        elif m_stru:
            stru_name = m_stru.group(1)
            new_lines.append(line)
            i += 1
            header_lines = []
            pos_found = False

            while i < len(source_lines):
                l_strip = source_lines[i].strip()
                if (
                    l_strip.startswith("NEW FRMWORK")
                    or l_strip.startswith("NEW EQUIPMENT")
                    or l_strip.startswith("NEW STRUCTURE")
                    or l_strip == "END"
                ):
                    break
                m_pos = re.match(r"^POS\s+(.+)", l_strip, re.IGNORECASE)
                if m_pos:
                    pos_found = True
                    orig_pos_str = m_pos.group(1)
                    e, n, u = parse_pos(orig_pos_str)
                    new_pos_str = format_pos(e + DE, n + DN, u + DU)
                    header_lines.append(new_pos_str)
                    records.append({
                        "type": "STRUCTURE",
                        "name": stru_name,
                        "old_pos": orig_pos_str,
                        "new_pos": new_pos_str,
                        "e_new": e + DE,
                        "n_new": n + DN,
                        "u_new": u + DU,
                    })
                else:
                    header_lines.append(source_lines[i])
                i += 1

            if not pos_found:
                new_pos_str = format_pos(DE, DN, DU)
                header_lines.insert(0, new_pos_str)
                records.append({
                    "type": "STRUCTURE",
                    "name": stru_name,
                    "old_pos": "None (0,0,0)",
                    "new_pos": new_pos_str,
                    "e_new": DE,
                    "n_new": DN,
                    "u_new": DU,
                })

            new_lines.extend(header_lines)
            continue

        new_lines.append(line)
        i += 1

    return new_lines, records


def run() -> None:
    src_path = repo_root / "Projects" / "JK-Tank_Build" / "imports" / "2026-09-02_WSB_TA.txt"
    src_lines = src_path.read_text(encoding="utf-8").splitlines()

    new_lines, records = transform(src_lines)
    new_text = "\n".join(new_lines) + "\n"

    out_dir = repo_root / "Projects" / "JK-Tank_Build" / "output"
    out_txt = out_dir / "WSB_TA_relocate_20260902.txt"
    out_pml = out_dir / "WSB_TA_relocate_20260902.pml"

    out_txt.write_text(new_text, encoding="utf-8")
    out_pml.write_text(new_text, encoding="utf-8")

    print(f"Original lines: {len(src_lines)}")
    print(f"Generated lines: {len(new_lines)}")
    print(f"Wrote text to: {out_txt}")
    print(f"Wrote PML to: {out_pml}")

    sha_src = hashlib.sha256(src_path.read_bytes()).hexdigest()
    sha_out = hashlib.sha256(out_pml.read_bytes()).hexdigest()
    print(f"Source SHA256: {sha_src}")
    print(f"Output SHA256: {sha_out}")

    err_src = validate_pml("\n".join(src_lines))
    err_new = validate_pml(new_text)
    print(f"validate_pml findings: Source={len(err_src)}, Output={len(err_new)} (New findings: {len(err_new) - len(err_src)})")

    # Unified diff check
    diff = list(difflib.unified_diff(src_lines, new_lines, fromfile="source", tofile="target", lineterm=""))
    additions = [d for d in diff if d.startswith("+") and not d.startswith("+++")]
    deletions = [d for d in diff if d.startswith("-") and not d.startswith("---")]
    print(f"Diff statistics: {len(deletions)} deletions, {len(additions)} additions")

    print("\n=== EQUIPMENT AND STRUCTURE RELOCATION AUDIT ===")
    for r in records:
        print(f"[{r['type']:<9}] {r['name']:<20}: {r['old_pos']}  -->  {r['new_pos']}")


if __name__ == "__main__":
    run()
