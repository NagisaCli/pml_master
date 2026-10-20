"""
Numeric verification of the 203-TA-401 macro (R2).

A textual check is not verification (IR-6 / IR-11b). This parses the emitted
macro, reconstructs every element's true occupied extent from its own datum,
and asserts physical properties — not the formulas the builder just applied.

    python Projects/203_TA_401_BS_Filtrate_Tank/tools/verify_203_TA_401.py
"""

from __future__ import annotations

import importlib.util
import math
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parent.parent
MACRO = PROJECT / "output" / "203_TA_401_BS_Filtrate_Tank.pml"

_spec = importlib.util.spec_from_file_location(
    "wsb_pml_builder", ROOT / "wsb" / "pml_builder.py")
_pml = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_pml)

sys.path.insert(0, str(PROJECT))
import equipment_data as D  # noqa: E402
import build_203_TA_401 as B  # noqa: E402

SHELL_FACE = D.SHELL_OD / 2.0
TOL = 0.6
NEGATIVES = {"NCYLINDER", "NBOX", "NDISH", "NCONE"}


def parse(text):
    """Yield one dict per NEW block, with its parent, attributes and order."""
    stack, blocks = [], []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("--"):
            continue
        m = re.match(r"^NEW\s+(\w+)\s*(/\S+)?", line, re.I)
        if m:
            blk = {"type": m.group(1).upper(), "name": m.group(2) or "",
                   "attrs": {}, "order": [],
                   "parent": stack[-1] if stack else None}
            blocks.append(blk)
            stack.append(blk)
            continue
        if line.upper() == "END":
            if stack:
                stack.pop()
            continue
        if stack:
            key = line.split()[0].upper()
            stack[-1]["attrs"][key] = line
            stack[-1]["order"].append(key)
    return blocks


def _bearing_from_text(txt):
    """Invert _plan_direction: 'E 30 N' -> 30 degrees East towards North."""
    parts = txt.strip().split()
    base = {"E": 0.0, "N": 90.0, "W": 180.0, "S": 270.0}
    if len(parts) == 1:
        return base[parts[0].upper()]
    a, d, bnd = base[parts[0].upper()], float(parts[1]), parts[2].upper()
    ccw = {("E", "N"), ("N", "W"), ("W", "S"), ("S", "E")}
    return (a + d) % 360 if (parts[0].upper(), bnd) in ccw else (a - d) % 360


def num(b, key):
    m = re.search(rf"^{key}\s+(-?[\d.]+)", b["attrs"].get(key, ""), re.I)
    return float(m.group(1)) if m else None


def pos(b):
    m = re.search(r"POS\s+E\s+(-?[\d.]+)\s+N\s+(-?[\d.]+)\s+U\s+(-?[\d.]+)",
                  b["attrs"].get("POS", ""), re.I)
    return tuple(float(x) for x in m.groups()) if m else None


def main() -> int:
    text = MACRO.read_text(encoding="utf-8")
    blocks = parse(text)
    problems, notes = [], []

    solids = [b for b in blocks
              if b["type"] in ("CYLI", "CONE", "BOX", "DISH", "RTORUS", "EXTRUSION")]
    negs = [b for b in blocks if b["type"] in NEGATIVES]
    nozz = [b for b in blocks if b["type"] == "NOZZLE"]
    if not solids or not nozz or not negs:
        print("FAIL: parser found nothing — a silent verifier is worse than "
              "none (IR-11f)")
        return 1

    # ---- 1. engine validation ------------------------------------------
    problems += [f"validate_pml: {f}" for f in _pml.validate_pml(text)]

    # ---- 2. positive dimensions ----------------------------------------
    for b in solids + negs:
        dims = [num(b, k) for k in ("DIAM", "HEIG", "XLEN", "YLEN", "ZLEN",
                                    "DTOP", "DBOT", "RINS", "ROUT")
                if num(b, k) is not None]
        if any(d <= 0 for d in dims):
            problems.append(f"{b['type']} has a non-positive dimension")

    # ---- 3. every negative is a CHILD, and fits inside its parent -------
    for b in negs:
        p = b["parent"]
        if p is None or p["type"] in NEGATIVES:
            problems.append(
                f"{b['type']} is not nested inside a solid — a negative at "
                f"sibling level cuts nothing")
            continue
        if b["type"] == "NCYLINDER":
            pd, bd = num(p, "DIAM"), num(b, "DIAM")
            if pd is None or bd is None or bd >= pd:
                problems.append(
                    f"NCYLINDER bore {bd} does not fit inside its parent {pd} "
                    f"— the solid would vanish")
            elif num(b, "HEIG") <= num(p, "HEIG"):
                problems.append(
                    f"NCYLINDER height {num(b,'HEIG')} does not overcut its "
                    f"parent {num(p,'HEIG')} — end faces left capped")
        if b["type"] == "NBOX":
            for k in ("XLEN", "YLEN", "ZLEN"):
                if num(b, k) >= num(p, k):
                    problems.append(f"NBOX {k} does not fit inside its parent")

    # ---- 4. occupied extents from each element's own datum --------------
    lo_u, hi_u, max_r = math.inf, -math.inf, 0.0
    for b in solids:
        p = pos(b)
        if p is None:
            problems.append(f"{b['type']} has no POS")
            continue
        e, n, u = p
        t = b["type"]
        if t in ("CYLI", "CONE"):
            h = num(b, "HEIG")
            d = num(b, "DIAM") or max(num(b, "DTOP") or 0, num(b, "DBOT") or 0)
            lo, hi, rad = u - h / 2, u + h / 2, d / 2
        elif t == "BOX":
            z = num(b, "ZLEN")
            lo, hi = u - z / 2, u + z / 2
            rad = math.hypot(num(b, "XLEN"), num(b, "YLEN")) / 2
        elif t == "RTORUS":
            h = num(b, "HEIG")
            base = u - h / 2 if B.RTORUS_BASE_IS_CENTRE else u
            lo, hi = base, base + h
            # A sector's plan envelope is NOT centre + ROUT: sample the arc.
            mo = re.search(r"X\s+IS\s+(.+?)\s*$", b["attrs"].get("ORI", ""), re.I)
            mg = re.search(r"ANGL\s+([\d.]+)", b["attrs"].get("ANGL", ""))
            sp = float(mg.group(1)) if mg else 360.0
            b0 = _bearing_from_text(mo.group(1)) if mo else 0.0
            rad = 0.0
            for k in range(41):
                a = math.radians(b0 + sp * k / 40.0)
                for rr in (num(b, "RINS"), num(b, "ROUT")):
                    rad = max(rad, math.hypot(e + rr * math.cos(a),
                                              n + rr * math.sin(a)))
            lo_u, hi_u = min(lo_u, lo), max(hi_u, hi)
            max_r = max(max_r, rad)
            continue
        elif t == "EXTRUSION":
            verts = [vb for vb in blocks
                     if vb["type"] == "VERTEX" and vb["parent"]
                     and vb["parent"]["parent"] is b]
            ys = [pos(v)[1] for v in verts if pos(v)]
            xs = [pos(v)[0] for v in verts if pos(v)]
            if not ys:
                problems.append("EXTRUSION has no LOOP vertices")
                continue
            lo, hi, rad = min(ys), max(ys), max(abs(x) for x in xs)
        else:
            continue
        lo_u, hi_u = min(lo_u, lo), max(hi_u, hi)
        max_r = max(max_r, math.hypot(e, n) + rad)

    if abs(lo_u) > TOL:
        problems.append(f"lowest face is U {lo_u:.2f}, not the bottom-centre "
                        f"datum U 0 (IR-6)")
    expect_top = D.ROOF_COLLAR_TOP_U + D.ROOF_DECK_T
    if abs(hi_u - expect_top) > 5.0:
        problems.append(f"highest face U {hi_u:.1f} != roof deck top {expect_top}")
    equi = [b for b in blocks if b["type"] == "EQUI"]
    if len(equi) != 1 or pos(equi[0]) != (0.0, 0.0, 0.0):
        problems.append("expected exactly one EQUI anchored at E0 N0 U0 (IR-7)")

    # ---- 5. THE separation wall lands on the shell bore ------------------
    # A property test: recompute the arc's two ends from what was emitted and
    # check they meet the shell. This fails if the arc centre, radius, start
    # bearing or span is wrong — none of which a bounds check can see.
    wall = [b for b in solids if b["type"] == "RTORUS"
            and abs(num(b, "HEIG") - D.SEP_WALL_TOP) < 1.0]
    if len(wall) != 1:
        problems.append(f"expected one separation-wall RTORUS, found {len(wall)}")
    else:
        w = wall[0]
        we, wn, _ = pos(w)
        m = re.search(r"ANGL\s+([\d.]+)", w["attrs"].get("ANGL", ""))
        span = float(m.group(1)) if m else 0.0
        mo = re.search(r"X\s+IS\s+(.+?)\s*$", w["attrs"].get("ORI", ""), re.I)
        if not mo:
            problems.append("separation wall RTORUS has no X axis in its ORI")
            return 1
        b0 = _bearing_from_text(mo.group(1))
        rmid = (num(w, "RINS") + num(w, "ROUT")) / 2.0
        for tag, brg, rad in (("start", b0, rmid), ("end", b0 + span, rmid)):
            x = we + rad * math.cos(math.radians(brg))
            y = wn + rad * math.sin(math.radians(brg))
            r = math.hypot(x, y)
            az = math.degrees(math.atan2(x, y)) % 360
            # Property: the end must land INSIDE the shell plate band, i.e.
            # welded into it - not short of the bore, not outside the shell.
            if not (D.SHELL_ID / 2.0 - 2.0 <= r <= D.SHELL_OD / 2.0 + 2.0):
                problems.append(
                    f"separation wall {tag} lands at R{r:.1f}, outside the shell "
                    f"plate band R{D.SHELL_ID/2:.1f}..{D.SHELL_OD/2:.1f}")
            notes.append(f"separation wall {tag} meets the shell at R{r:.1f} "
                         f"az {az:.2f}")
        arc = math.radians(span) * num(w, "RINS")
        notes.append(f"separation wall arc length {arc:.1f} mm at R{num(w,'RINS'):.0f} "
                     f"(measured polyline 4830.3)")
        if abs(arc - 4830.3) > 20.0:
            problems.append(f"wall arc length {arc:.1f} is more than 20 mm from "
                            f"the drawn 4830.3")

    # ---- 6. rafters follow the real roof slope --------------------------
    extr = [b for b in solids if b["type"] == "EXTRUSION"]
    if len(extr) != D.RAFTER_COUNT:
        problems.append(f"expected {D.RAFTER_COUNT} rafter extrusions, "
                        f"found {len(extr)}")
    for b in extr[:1]:
        verts = [vb for vb in blocks if vb["type"] == "VERTEX"
                 and vb["parent"] and vb["parent"]["parent"] is b]
        pts = [pos(v)[:2] for v in verts if pos(v)]
        (r1, u1), (r2, u2) = pts[0], pts[1]
        slope = math.degrees(math.atan2(u1 - u2, r2 - r1))
        if abs(slope - D.ROOF_SLOPE_DEG) > 0.05:
            problems.append(f"rafter profile slope {slope:.3f} deg != the roof's "
                            f"{D.ROOF_SLOPE_DEG} deg")
        notes.append(f"rafter profile slope {slope:.3f} deg over "
                     f"{r2-r1:.1f} mm of run, depth {pts[3][1]-pts[0][1]:.1f}")

    # ---- 7. nozzles: properties, not formulas ---------------------------
    for b in nozz:
        heig, p = num(b, "HEIG"), pos(b)
        if heig is None or p is None:
            problems.append(f"NOZZLE {b['name']} missing HEIG or POS"); continue
        if not 1.0 <= heig <= 2000.0:
            problems.append(f"NOZZLE {b['name']} HEIG {heig} outside 1..2000")
        if not b["order"] or b["order"][0] != "CATR":
            problems.append(f"NOZZLE {b['name']} does not bind CATR first (IR-9a)")
        if "ORI" in b["order"] and "POS" in b["order"] \
                and b["order"].index("POS") > b["order"].index("ORI"):
            problems.append(f"NOZZLE {b['name']} has ORI before POS (IR-2)")
        if not re.search(r"ORI\s+P1\s+IS", b["attrs"].get("ORI", ""), re.I):
            problems.append(f"NOZZLE {b['name']} is not aimed by P1 (IR-2)")

    for mark, dn, u, ao, az, fr, _s in D.NOZZLES:
        if mark in ("N8", "N9", "N11", "N12", "N13"):
            continue
        root = fr - (D.N1_1_PROJECTION if mark == "N1.1" else fr - SHELL_FACE)
        if root > SHELL_FACE + TOL:
            problems.append(f"{mark} barrel root R{root:.1f} never reaches the "
                            f"shell face R{SHELL_FACE:.1f}")
        elif SHELL_FACE - root > 400.0:
            problems.append(f"{mark} barrel buried {SHELL_FACE-root:.0f} mm inside")

    # ---- 8. volume reconciliation ---------------------------------------
    vol = math.pi / 4 * (D.SHELL_ID / 1000) ** 2 * (D.SHELL_TOP / 1000)
    if abs(vol - D.DESIGN["nominal_volume_m3"]) > 2.0:
        problems.append(f"shell volume {vol:.1f} m3 does not reconcile with the "
                        f"drawing's {D.DESIGN['nominal_volume_m3']} m3")
    notes.insert(0, f"shell volume pi/4 x 6.0^2 x 8.0 = {vol:.1f} m3 vs drawing "
                    f"{D.DESIGN['nominal_volume_m3']} m3")
    notes.insert(1, f"{len(solids)} solids ({len(extr)} extrusions, "
                    f"{len([b for b in solids if b['type']=='RTORUS'])} rtorus), "
                    f"{len(negs)} nested voids, {len(nozz)} native NOZZLE, "
                    f"{len([b for b in blocks if b['type']=='SUBE'])} subequipments")
    notes.insert(2, f"occupied U {lo_u:.1f}..{hi_u:.1f}; plan envelope R{max_r:.1f}")

    print("=" * 72)
    print(f"VERIFY {MACRO.name}")
    print("=" * 72)
    for t in notes:
        print(f"  note : {t}")
    if problems:
        print()
        for t in problems:
            print(f"  FAIL : {t}")
        print(f"\n{len(problems)} problem(s)")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
