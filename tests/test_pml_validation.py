"""
PML macro syntax and E3D runtime constraint validation test.

Guards against recurring E3D fatal errors:
1. (42,88) Angles for TORI must be in the range 0 to 180.
2. (2,201) Primitive attributes (XLEN, DIAM, etc.) executed on SUBEQUIPMENT or outside a primitive.
3. Illegal consecutive NEW statements without END.
4. Unbalanced element stacks.
5. Forbidden prologue keywords (SUSPEND, RESUME, VAR, ALPHA).
6. PML2 constructs (!var, COLLECT, UNSET, ENDS, !!Alert).
"""

from __future__ import annotations

import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

PRIM_ATTRIBS = {
    'BOX': {'XLEN', 'YLEN', 'ZLEN', 'POS', 'ORI'},
    'NBOX': {'XLEN', 'YLEN', 'ZLEN', 'POS', 'ORI'},
    'CYLINDER': {'DIAM', 'HEIG', 'POS', 'ORI'},
    'NCYLINDER': {'DIAM', 'HEIG', 'POS', 'ORI'},
    'CONE': {'DTOP', 'DBOT', 'HEIG', 'OFFS', 'POS', 'ORI'},
    'NCONE': {'DTOP', 'DBOT', 'HEIG', 'OFFS', 'POS', 'ORI'},
    'DISH': {'DIAM', 'HEIG', 'RADI', 'POS', 'ORI'},
    'NDISH': {'DIAM', 'HEIG', 'RADI', 'POS', 'ORI'},
    'PYRAMID': {'XBOT', 'YBOT', 'XTOP', 'YTOP', 'XOFF', 'YOFF', 'HEIG', 'POS', 'ORI'},
    'NPYRAMID': {'XBOT', 'YBOT', 'XTOP', 'YTOP', 'XOFF', 'YOFF', 'HEIG', 'POS', 'ORI'},
    'CTORUS': {'RINS', 'ROUT', 'ANGL', 'POS', 'ORI'},
    'RTORUS': {'RINS', 'ROUT', 'HEIG', 'ANGL', 'POS', 'ORI'},
    'SNOUT': {'DTOP', 'DBOT', 'HEIG', 'OFFS', 'POS', 'ORI'},
    'EXTRUSION': {'HEIG', 'POS', 'ORI'},
    'NXTRUSION': {'HEIG', 'POS', 'ORI'},
    'LOOP': set(),
    'VERTEX': {'POS'},
    'SUBEQUIPMENT': {'POS', 'ORI', 'BUIL', 'DSCO', 'PTSP', 'INSC'},
    'EQUIPMENT': {'POS', 'ORI', 'PURP', 'BUIL', 'DSCO', 'PTSP', 'INSC'},
    'NOZZLE': {'POS', 'ORI', 'CATR', 'CREF', 'BARR', 'INSC', 'DSCO', 'BUIL', 'PTSP', 'PAVE', 'PCOA', 'PBAX', 'PAAX', 'POFF', 'BOFF', 'PSPE', 'HEIG'}
}


def validate_pml(pml_path: Path) -> list[str]:
    with open(pml_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    errors = []
    stack = []
    last_cmd = None
    last_target = None

    for idx, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith('--') or line.startswith('$*'):
            continue
        parts = line.split()
        cmd = parts[0].upper()

        # 1. PML2 check
        if any(line.startswith(p) for p in ['!var', 'COLLECT', 'UNSET', 'ENDS', 'END EQUI', '!!']):
            errors.append(f'Line {idx}: PML2 syntax not allowed: {line}')

        # 2. Forbidden macro keywords
        if cmd in {'SUSPEND', 'RESUME', 'VAR', 'ALPHA'}:
            errors.append(f'Line {idx}: Forbidden render prologue command: {cmd}')

        # 3. (42,88) angle check
        if cmd == 'ANGL':
            m = re.search(r'ANGL\s+([0-9.]+)', line, re.IGNORECASE)
            if m:
                ang = float(m.group(1))
                if ang > 180 or ang <= 0:
                    errors.append(f'Line {idx}: (42,88) ANGL {ang} out of range (0, 180]: {line}')

        # 4. Hierarchy and stack check
        if cmd == 'NEW':
            target = parts[1].upper() if len(parts) > 1 else ''
            if last_cmd == 'NEW' and not (last_target == 'LOOP' and target == 'VERTEX'):
                errors.append(f'Line {idx}: Illegal consecutive NEW: {last_target} -> {target}')
            stack.append((target, idx))
            last_cmd = 'NEW'
            last_target = target
        elif cmd == 'OLD':
            pass
        elif cmd == 'END':
            if not stack:
                errors.append(f'Line {idx}: END with empty stack')
            else:
                stack.pop()
            last_cmd = 'END'
        elif cmd in {'XLEN', 'YLEN', 'ZLEN', 'HEIG', 'DIAM', 'DTOP', 'DBOT', 'RINS', 'ROUT', 'RADI', 'XBOT', 'YBOT', 'XTOP', 'YTOP', 'ANGL'}:
            if last_cmd == 'END':
                errors.append(f'Line {idx}: Attribute {cmd} immediately follows END without NEW (will trigger (2,201))')
            curr = stack[-1][0] if stack else 'NONE'
            valid = PRIM_ATTRIBS.get(curr, set())
            if cmd not in valid:
                errors.append(f'Line {idx}: Attribute {cmd} invalid on {curr}')
            last_cmd = cmd
        else:
            last_cmd = cmd

    if stack:
        errors.append(f'Unclosed elements on stack at EOF: {stack}')
    return errors


def test_optimized_pump_macro_syntax():
    pump_macro = REPO_ROOT / "Projects" / "JK_Pump_Build" / "output" / "205_PU_054_optimized_20260904.pml"
    assert pump_macro.is_file(), f"{pump_macro} does not exist"
    errs = validate_pml(pump_macro)
    assert not errs, f"Validation failed with {len(errs)} errors:\n" + "\n".join(errs[:10])
