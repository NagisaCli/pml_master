"""
203-TA-019 Retrofit Generator (Rev 2 - 2026-09-15)
==================================================
Updates:
1. Equipment & Structure position WRT owner updated to live project coordinates:
   POS E 52402.88mm N 58697.69mm U 0mm (Owner: ZONE /WSB_TA)
2. Removed batch dump envelope (INPUT BEGIN, INPUT FINISH, ONERROR GOLABEL /ERROR3)
   which caused syntax errors during interactive $m execution.
3. Clean native PML1 structure:
   - Sets Current Element to /WSB_TA at line 1.
   - Creates NEW EQUIPMENT /203_TA_019 first.
   - Creates NEW STRUCTURE /203_TA_019_STRU second.
   - Trailing pipe branch tail rebindings.
4. Generates:
   - Combined macro: WSB_TA_203_TA_019_retrofit_20260914.pml
   - Equipment-only macro: WSB_TA_203_TA_019_EQUI_20260914.pml
   - Structure-only macro: WSB_TA_203_TA_019_STRU_20260914.pml
"""

import math
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
ALT_EXPORT = Path(r"C:\Users\A\.gemini\antigravity\brain\55927096-4ebf-4e09-8ce4-336c7c879052\.user_uploaded\media_1789383959828.txt")
OUTPUT_DIR = ROOT_DIR / "Projects" / "JK-Tank_Build" / "output"
COMBINED_PML = OUTPUT_DIR / "WSB_TA_203_TA_019_retrofit_20260914.pml"
EQUI_PML = OUTPUT_DIR / "WSB_TA_203_TA_019_EQUI_20260914.pml"
STRU_PML = OUTPUT_DIR / "WSB_TA_203_TA_019_STRU_20260914.pml"

# Root container position WRT Owner /WSB_TA
ROOT_POS_LINE = "POS E 52402.88mm N 58697.69mm U 0mm"

def build_walkway_loop(r_in=1000.0, r_out=1900.0, slot_half_width=250.0, num_steps=32):
    y_in_slot = -math.sqrt(r_in**2 - slot_half_width**2)    # -968.25 mm
    y_out_slot = -math.sqrt(r_out**2 - slot_half_width**2)  # -1883.48 mm

    theta_out_start = math.atan2(y_out_slot, slot_half_width)
    theta_out_end = math.atan2(y_out_slot, -slot_half_width)
    if theta_out_end < theta_out_start:
        theta_out_end += 2 * math.pi

    theta_in_start = math.atan2(y_in_slot, -slot_half_width)
    theta_in_end = math.atan2(y_in_slot, slot_half_width)
    if theta_in_start < theta_in_end:
        theta_in_start += 2 * math.pi

    def fmt_pos(x, y):
        e_str = f"E {x:.1f}mm" if x >= 0 else f"W {-x:.1f}mm"
        n_str = f"N {y:.1f}mm" if y >= 0 else f"S {-y:.1f}mm"
        if e_str == "W 0.0mm": e_str = "E 0mm"
        if n_str == "S 0.0mm": n_str = "N 0mm"
        return f"POS {e_str} {n_str} U 0mm"

    lines = ["NEW LOOP", ""]
    # 1. East inner slot corner
    lines += ["NEW VERTEX", fmt_pos(slot_half_width, y_in_slot), "", "END"]
    # 2. East outer slot corner
    lines += ["NEW VERTEX", fmt_pos(slot_half_width, y_out_slot), "", "END"]
    # 3. Outer circle counter-clockwise
    for i in range(1, num_steps):
        t = theta_out_start + (theta_out_end - theta_out_start) * (i / num_steps)
        lines += ["NEW VERTEX", fmt_pos(r_out * math.cos(t), r_out * math.sin(t)), "", "END"]
    # 4. West outer slot corner
    lines += ["NEW VERTEX", fmt_pos(-slot_half_width, y_out_slot), "", "END"]
    # 5. West inner slot corner
    lines += ["NEW VERTEX", fmt_pos(-slot_half_width, y_in_slot), "", "END"]
    # 6. Inner circle clockwise
    for i in range(1, num_steps):
        t = theta_in_start - (theta_in_start - theta_in_end) * (i / num_steps)
        lines += ["NEW VERTEX", fmt_pos(r_in * math.cos(t), r_in * math.sin(t)), "", "END"]
    lines.append("END")
    return lines

def build_radial_brackets():
    center_e, center_n, u_val, r_mid = 15445.0, 6415.0, 7875.0, 1450.0
    brackets = [
        (0.0, "ORI Z IS U AND X IS N"),
        (45.0, "ORI Z IS U AND X IS N 45 E"),
        (90.0, "ORI Z IS U AND X IS E"),
        (270.0, "ORI Z IS U AND X IS W"),
        (315.0, "ORI Z IS U AND X IS N 45 W"),
    ]
    lines = []
    for bearing, ori in brackets:
        rad = math.radians(bearing)
        lines += [
            "NEW BOX",
            "XLEN 880mm",
            "YLEN 12mm",
            "ZLEN 250mm",
            ori,
            f"POS E {center_e + r_mid * math.sin(rad):.1f}mm N {center_n + r_mid * math.cos(rad):.1f}mm U {u_val:.0f}mm",
            "",
            "END",
        ]
    return lines

def generate_all_macros():
    with open(ALT_EXPORT, "r", encoding="utf-8-sig") as f:
        full_text = f.read()

    end_idx = full_text.find("-- End Data Listing")
    text = full_text[:end_idx] if end_idx != -1 else full_text
    raw_lines = [l.rstrip("\r\n") for l in text.splitlines()]

    # Find key indices
    stru_start = None
    equi_start = None
    old_start = None
    for i, l in enumerate(raw_lines):
        if l.startswith("NEW STRUCTURE /203_TA_019_STRU"):
            stru_start = i
        elif l.startswith("NEW EQUIPMENT /203_TA_019"):
            equi_start = i
        elif l.startswith("OLD NOZZLE"):
            old_start = i
            break

    # 1. Build STRUCTURE block
    # Handrail A & B
    handrail_a_lines = [
        "NEW HANDRA /203_TA_019_TOP_HANDRAIL_A",
        "POS E 15445mm N 6415mm U 8050mm",
        "RAILHE 1100mm 550mm",
        "POSTSP 1000mm",
        "TANGOF 300mm",
        "SHOWKP true",
        "BRAD 100mm",
        "FIRE 0",
        "BUIL false",
        "SHOP false",
        "",
        "NEW RPATH",
        "DRNS S 0.9999 W",
        "DRNE E",
        "",
        "NEW POINTR",
        "POS W 240mm S 1250mm U 0mm",
        "FRAD 100mm",
        "",
        "END",
        "NEW POINTR",
        "POS W 250mm S 1822.94mm U 0mm",
        "FRAD 100mm",
        "",
        "END",
        "NEW CURVE",
        "POS W 1026.37mm S 1527.14mm U 0mm",
        "CURTYP THRU",
        "",
        "END",
        "NEW POINTR",
        "POS W 1840mm N 0mm U 0mm",
        "FRAD 100mm",
        "",
        "END",
        "NEW CURVE",
        "POS W 1301.08mm N 1301.08mm U 0mm",
        "CURTYP THRU",
        "",
        "END",
        "NEW POINTR",
        "POS E 0mm N 1840mm U 0mm",
        "FRAD 100mm",
        "",
        "END",
        "END",
        "END",
    ]

    handrail_b_lines = [
        "NEW HANDRA /203_TA_019_TOP_HANDRAIL_B",
        "POS E 15445mm N 6415mm U 8050mm",
        "RAILHE 1100mm 550mm",
        "POSTSP 1000mm",
        "TANGOF 300mm",
        "SHOWKP true",
        "BRAD 100mm",
        "FIRE 0",
        "BUIL false",
        "SHOP false",
        "",
        "NEW RPATH",
        "DRNS S 0.9999 E",
        "DRNE W",
        "",
        "NEW POINTR",
        "POS E 240mm S 1250mm U 0mm",
        "FRAD 100mm",
        "",
        "END",
        "NEW POINTR",
        "POS E 250mm S 1822.94mm U 0mm",
        "FRAD 100mm",
        "",
        "END",
        "NEW CURVE",
        "POS E 1026.37mm S 1527.14mm U 0mm",
        "CURTYP THRU",
        "",
        "END",
        "NEW POINTR",
        "POS E 1840mm N 0mm U 0mm",
        "FRAD 100mm",
        "",
        "END",
        "NEW CURVE",
        "POS E 1301.08mm N 1301.08mm U 0mm",
        "CURTYP THRU",
        "",
        "END",
        "NEW POINTR",
        "POS E 0mm N 1840mm U 0mm",
        "FRAD 100mm",
        "",
        "END",
        "END",
        "END",
    ]

    # Find Return A start in raw_lines
    ret_a_start = None
    for i in range(stru_start, equi_start):
        if "NEW HANDRA /203_TA_019_TOP_RETURN_A" in raw_lines[i]:
            ret_a_start = i
            break

    stru_block = [
        "NEW STRUCTURE /203_TA_019_STRU",
        ROOT_POS_LINE,
        "BUIL false",
        "PDNAME unset",
        "",
        "NEW FRMWORK /203_TA_019_FRMWORK",
        "BUIL false",
        "SHOP false",
        "GRADE 0",
        "FIRE 0",
        "PTSP unset",
        "INSC unset",
        "PDNAME unset",
        "",
    ] + handrail_a_lines + handrail_b_lines + raw_lines[ret_a_start:equi_start]

    # 2. Build EQUIPMENT block
    # Modify Dropleg in SHELL
    first_dish = None
    for i in range(equi_start, len(raw_lines)):
        if "NEW SUBEQUIPMENT /203_TA_019_SHELL" in raw_lines[i]:
            for j in range(i+1, i+15):
                if "NEW DISH" in raw_lines[j]:
                    first_dish = j
                    break
            break

    dropleg_lines = [
        "NEW CYLINDER",
        "DIAM 1050mm",
        "HEIG 50mm",
        "ORI Z IS U AND Y IS N",
        "POS E 15445mm N 6415mm U 25mm",
        "",
        "END",
        "NEW CYLINDER",
        "DIAM 800mm",
        "HEIG 1950mm",
        "ORI Z IS U AND Y IS N",
        "POS E 15445mm N 6415mm U 1025mm",
        "",
        "END",
    ]

    # Modify N9 POS
    n9_pos_idx = None
    for i in range(equi_start, len(raw_lines)):
        if "NEW NOZZLE /203_TA_019_N9_NOZZ" in raw_lines[i]:
            for j in range(i+1, i+5):
                if raw_lines[j].startswith("POS E 14888.5mm"):
                    n9_pos_idx = j
                    break
            break

    # Modify Walkway
    walkway_start = None
    walkway_end = None
    for i in range(equi_start, len(raw_lines)):
        if "NEW EXTRUSION" in raw_lines[i] and i+1 < len(raw_lines) and "U 8000mm" in raw_lines[i+1]:
            walkway_start = i
            for j in range(i+2, len(raw_lines)):
                if raw_lines[j].startswith("NEW BOX"):
                    walkway_end = j
                    break
            break

    brackets_end = None
    for i in range(walkway_end, len(raw_lines)):
        if "U 8550mm" in raw_lines[i]:
            for k in range(i, walkway_end, -1):
                if raw_lines[k] == "NEW BOX":
                    brackets_end = k
                    break
            break

    walkway_lines = [
        "NEW EXTRUSION",
        "POS E 15445mm N 6415mm U 8000mm",
        "HEIG 50mm",
        "",
    ] + build_walkway_loop() + ["END"]

    new_bracket_lines = build_radial_brackets()

    equi_block = [
        "NEW EQUIPMENT /203_TA_019",
        "FUNC '001024'",
        ROOT_POS_LINE,
        "BUIL false",
        "DSCO unset",
        "PTSP unset",
        "INSC unset",
        "",
    ]
    # from after 'INSC unset' of equi root to first_dish
    # in raw_lines, equi_start+1 to +6 are attributes
    equi_attrs_end = equi_start + 7
    while raw_lines[equi_attrs_end] == "":
        equi_attrs_end += 1

    equi_block += raw_lines[equi_attrs_end:first_dish]
    equi_block += dropleg_lines
    equi_block += raw_lines[first_dish:n9_pos_idx]
    equi_block.append("POS E 16001.5mm N 6415mm U 500mm")
    equi_block += raw_lines[n9_pos_idx+1:walkway_start]
    equi_block += walkway_lines
    equi_block += raw_lines[walkway_end:brackets_end]
    equi_block += new_bracket_lines
    equi_block += raw_lines[brackets_end:old_start] # includes closing END of /203_TA_019

    # 3. Piping branch rebindings
    pipe_rebind_lines = [
        "OLD NOZZLE 1 of SUBEQUIPMENT /203_TA_019_N2",
        "CREF BRANCH /203-PUW-600-P12-2460-150/B1  TAIL",
        "CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033",
        "",
        "OLD NOZZLE /203_TA_019_N1_NOZZ",
        "CREF BRANCH /203-POD-350-P12-2501-150/B1  TAIL",
        "CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0XX",
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Emit Combined Macro
    comb_header = [
        "-- ====================================================================",
        "-- Macro: WSB_TA_203_TA_019_retrofit_20260914.pml",
        "-- Equipment: /203_TA_019 (Oxygen Stage Feed Tank)",
        "-- Structure: /203_TA_019_STRU (Top Walkway Handrails)",
        "-- Owner: ZONE WSB_TA",
        f"-- {ROOT_POS_LINE}",
        "-- ====================================================================",
        "",
        "-- 1. EQUIPMENT: /203_TA_019",
    ]
    comb_lines = comb_header + equi_block + ["", "-- 2. STRUCTURE: /203_TA_019_STRU"] + stru_block + ["", "-- 3. Branch Rebinding"] + pipe_rebind_lines
    with open(COMBINED_PML, "w", encoding="utf-8") as f:
        f.write("\n".join(comb_lines) + "\n")

    # Emit Equipment Only Macro
    equi_header = [
        "-- ====================================================================",
        "-- Equipment Macro: WSB_TA_203_TA_019_EQUI_20260914.pml",
        "-- Equipment: /203_TA_019 (Oxygen Stage Feed Tank)",
        "-- Owner: ZONE WSB_TA",
        f"-- {ROOT_POS_LINE}",
        "-- Contains: 360-deg walkway, 9 brackets, DN800 dropleg, East N9",
        "-- ====================================================================",
        "",
    ]
    equi_only_lines = equi_header + equi_block + ["", "-- Branch Rebinding"] + pipe_rebind_lines
    with open(EQUI_PML, "w", encoding="utf-8") as f:
        f.write("\n".join(equi_only_lines) + "\n")

    # Emit Structure Only Macro
    stru_header = [
        "-- ====================================================================",
        "-- Structure Macro: WSB_TA_203_TA_019_STRU_20260914.pml",
        "-- Structure: /203_TA_019_STRU (Top Walkway Handrails A & B)",
        "-- Owner: ZONE WSB_TA",
        f"-- {ROOT_POS_LINE}",
        "-- ====================================================================",
        "",
    ]
    stru_only_lines = stru_header + stru_block
    with open(STRU_PML, "w", encoding="utf-8") as f:
        f.write("\n".join(stru_only_lines) + "\n")

    print(f"Generated Combined:  {COMBINED_PML} ({len(comb_lines)} lines)")
    print(f"Generated Equipment: {EQUI_PML} ({len(equi_only_lines)} lines)")
    print(f"Generated Structure: {STRU_PML} ({len(stru_only_lines)} lines)")

if __name__ == "__main__":
    generate_all_macros()
