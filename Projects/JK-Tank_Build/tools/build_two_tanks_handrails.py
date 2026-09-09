"""
Replace the old cylinder top handrails in the two-tank data listing
with the new native structural HANDRA/RPATH elements with ladder openings.
"""

from pathlib import Path
import re
import math

from wsb.pml_builder import validate_pml

def build_open_circular_handrail(name: str, pos_e: float, pos_n: float, pos_u: float, radius: float, rail_h1: float = 1100.0, rail_h2: float = 550.0) -> str:
    s_87 = math.sin(math.radians(87.0))
    c_87 = math.cos(math.radians(87.0))
    s_43_5 = math.sin(math.radians(43.5))
    c_43_5 = math.cos(math.radians(43.5))
    s_130_5 = math.sin(math.radians(130.5))
    c_130_5 = math.cos(math.radians(130.5))
    s_174 = math.sin(math.radians(174.0))
    c_174 = math.cos(math.radians(174.0))

    pos_clause = f"POS E {pos_e:.2f}mm N {pos_n:.2f}mm U {pos_u:.2f}mm" if pos_n >= 0 else f"POS E {pos_e:.2f}mm S {-pos_n:.2f}mm U {pos_u:.2f}mm"
    
    # Format numbers to eliminate trailing .00 if integer
    def f(val: float) -> str:
        r = round(val, 2)
        if abs(r - round(r)) < 1e-6:
            return f"{int(round(r))}"
        return f"{r:.2f}".rstrip('0').rstrip('.')

    lines = [
        f"NEW HANDRA /{name}",
        f"{pos_clause}",
        f"RAILHE {f(rail_h1)}mm {f(rail_h2)}mm",
        "POSTSP 1000mm",
        "TANGOF 300mm",
        "SHOWKP true",
        "BRAD 100mm",
        "FIRE 0",
        "BUIL false",
        "SHOP false",
        "",
        "NEW RPATH",
        "DRNS N 6 E",
        "DRNE S 6 E",
        "",
        "NEW POINTR",
        f"POS W {f(radius * c_174)}mm S {f(radius * s_174)}mm U 0mm",
        "FRAD 100mm",
        "END",
        "NEW CURVE",
        f"POS W {f(radius * -c_130_5)}mm S {f(radius * s_130_5)}mm U 0mm",
        "CURTYP THRU",
        "END",
        "NEW POINTR",
        f"POS E {f(radius * c_87)}mm S {f(radius * s_87)}mm U 0mm",
        "FRAD 100mm",
        "END",
        "NEW CURVE",
        f"POS E {f(radius * c_43_5)}mm S {f(radius * s_43_5)}mm U 0mm",
        "CURTYP THRU",
        "END",
        "NEW POINTR",
        f"POS E {f(radius)}mm N 0mm U 0mm",
        "FRAD 100mm",
        "END",
        "NEW CURVE",
        f"POS E {f(radius * c_43_5)}mm N {f(radius * s_43_5)}mm U 0mm",
        "CURTYP THRU",
        "END",
        "NEW POINTR",
        f"POS E {f(radius * c_87)}mm N {f(radius * s_87)}mm U 0mm",
        "FRAD 100mm",
        "END",
        "NEW CURVE",
        f"POS W {f(radius * -c_130_5)}mm N {f(radius * s_130_5)}mm U 0mm",
        "CURTYP THRU",
        "END",
        "NEW POINTR",
        f"POS W {f(radius * c_174)}mm N {f(radius * s_174)}mm U 0mm",
        "FRAD 100mm",
        "END",
        "END",
        "END",
    ]
    return "\n".join(lines)


def run():
    source_path = Path("Projects/JK-Tank_Build/imports/2026-08-31_two_tanks_native.txt")
    text = source_path.read_text(encoding="utf-8")

    hr_056_body = build_open_circular_handrail(
        name="205_TA_056_TOP_HANDRAIL_BODY",
        pos_e=67030.0,
        pos_n=21008.0,
        pos_u=26400.0,
        radius=4850.0,
    )
    new_sube_056 = f"""NEW SUBEQUIPMENT /205_TA_056_TOP_HANDRAIL
FUNC '001024'
BUIL false
DSCO unset
PTSP unset
INSC unset

{hr_056_body}
END"""

    hr_001_body = build_open_circular_handrail(
        name="205_TA_001_TOP_HANDRAIL_BODY",
        pos_e=26863.0,
        pos_n=-11601.0,
        pos_u=26400.0,
        radius=5300.0,
    )
    new_sube_001 = f"""NEW SUBEQUIPMENT /205_TA_001_TOP_HANDRAIL
FUNC '001024'
BUIL false
DSCO unset
PTSP unset
INSC unset

{hr_001_body}
END"""

    # Replace old /205_TA_056_TOP_HANDRAIL block
    pattern_056 = re.compile(r"NEW SUBEQUIPMENT /205_TA_056_TOP_HANDRAIL.*?END\s*\n(?=NEW CYLINDER|NEW SUBEQUIPMENT|NEW EQUIPMENT|OLD NOZZLE)", re.DOTALL)
    match_056 = pattern_056.search(text)
    if not match_056:
        raise ValueError("Could not find /205_TA_056_TOP_HANDRAIL block")
    
    text = text[:match_056.start()] + new_sube_056 + "\n" + text[match_056.end():]

    # Replace old /205_TA_001_TOP_HANDRAIL block
    pattern_001 = re.compile(r"NEW SUBEQUIPMENT /205_TA_001_TOP_HANDRAIL.*?END\s*\n(?=NEW SUBEQUIPMENT /205_TA_001_INTERNALS|NEW CYLINDER|NEW SUBEQUIPMENT|NEW EQUIPMENT|OLD NOZZLE)", re.DOTALL)
    match_001 = pattern_001.search(text)
    if not match_001:
        raise ValueError("Could not find /205_TA_001_TOP_HANDRAIL block")

    text = text[:match_001.start()] + new_sube_001 + "\n" + text[match_001.end():]

    out_path = Path("Projects/JK-Tank_Build/output/WSB_TA_handrails_20260831.txt")
    out_path.write_text(text, encoding="utf-8")
    print(f"Written output to {out_path} ({len(text.splitlines())} lines).")

    errors = validate_pml(text)
    if errors:
        print("PML Validation errors:", errors)
    else:
        print("PML Validation: CLEAN!")


if __name__ == "__main__":
    run()
