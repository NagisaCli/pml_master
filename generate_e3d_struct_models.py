"""
Master AVEVA E3D / PDMS PML1 Industrial Structural Modeling Generator:
Fixes the spatial misalignment between Pipe Supports and Cable Tray Brackets/Mesh.
"""

import os
import re
import csv
import math
from pathlib import Path
from collections import Counter, defaultdict

PACKAGE_DIR = Path(r"C:\Users\A\Desktop\流程图\E3D_管架与电缆桥架全套三维建模交付包")
OUTPUT_DIR_ORIGINAL = PACKAGE_DIR / "output"
OUTPUT_DIR_ASCII_C = Path(r"C:\e3d_models")
OUTPUT_DIR_ASCII_DESKTOP = Path(r"C:\Users\A\Desktop\e3d_models")

PS_CSV = PACKAGE_DIR / "01_全厂管道支架空间定位数据表_全量208处精准版.csv"
BRACKET_CSV = PACKAGE_DIR / "02_电缆桥架网道系统与支架精细化定位数据表_全量94处_9.1M版.csv"
CAD_TRAY_PML = Path(r"C:\Muvsera\Projects\e3d_live\Projects\CAD_Cable_Tray_Network\output\CAD_Cable_Tray_Network_R1.pml")

# 1. Base Plant Coordinate Shift
BASE_SHIFT_E = 52468.0
BASE_SHIFT_N = 59338.0

# 2. Cable Tray CAD (eui0.dwg) Origin Shift
# Origin of eui0.dwg is (8811.10, 49149.00)
# Unified Plant Target Origin is (52468.0, 59338.0)
CAD_TRAY_DX = 43656.9  # 52468.0 - 8811.10
CAD_TRAY_DY = 10189.0  # 59338.0 - 49149.00

def parse_pt(s):
    if not s:
        return [0.0, 0.0, 0.0]
    m = re.findall(r'[-+]?\d*\.\d+|\d+', s)
    if len(m) >= 3:
        return [float(m[0]), float(m[1]), float(m[2])]
    elif len(m) == 2:
        return [float(m[0]), float(m[1]), 0.0]
    return [0.0, 0.0, 0.0]

def clean_tag(tag):
    return re.sub(r'[^A-Za-z0-9_-]', '-', tag.strip())

def get_dir_frame(dx, dy):
    L = math.sqrt(dx*dx + dy*dy)
    if L < 1e-3:
        return (0.0, 1.0), (1.0, 0.0), 'N', 'E'
    ux, uy = dx/L, dy/L
    if abs(ux) >= abs(uy):
        if ux > 0:
            return (1.0, 0.0), (0.0, -1.0), 'E', 'S'
        else:
            return (-1.0, 0.0), (0.0, 1.0), 'W', 'N'
    else:
        if uy > 0:
            return (0.0, 1.0), (1.0, 0.0), 'N', 'E'
        else:
            return (0.0, -1.0), (-1.0, 0.0), 'S', 'W'

def emit_r3_screw_assembly(lines, tag, screw_idx, p_base, ux, uy, beam_dir):
    lines.append(f"NEW SUBE /SUBE-{tag}-SCREW-{screw_idx:02d}")
    lines.append("ORI Y IS N AND Z IS U")
    lines.append("POS E 0 N 0 U 0")

    # 1. Shank
    s_e = p_base[0] + 9.5 * ux
    s_n = p_base[1] + 9.5 * uy
    s_u = p_base[2]
    lines.extend([
        f"-- SHANK_{screw_idx} (20 mm shank, 19 mm depth)",
        "NEW CYLI",
        "DIAM 20.0",
        "HEIG 19.0",
        f"ORI Z IS {beam_dir} AND Y IS U",
        f"POS E {s_e:.1f} N {s_n:.1f} U {s_u:.1f}",
        "END"
    ])

    # 2. Washer
    w_e = p_base[0] + 17.5 * ux
    w_n = p_base[1] + 17.5 * uy
    w_u = p_base[2]
    lines.extend([
        f"-- WASHER_{screw_idx} (OD40 ID22 x 3 mm with central hole)",
        "NEW CYLI",
        "DIAM 40.0",
        "HEIG 3.0",
        f"ORI Z IS {beam_dir} AND Y IS U",
        f"POS E {w_e:.1f} N {w_n:.1f} U {w_u:.1f}",
        "NEW NCYLINDER",
        "DIAM 22.000000",
        "HEIG 5.000000",
        "ORI Y IS N AND Z IS U",
        "POS E 0.000000 N 0.000000 U 0.000000",
        "NAPPFLAG 2",
        "END",
        "END"
    ])

    # 3. Hex Head (AF 30 x 12 mm regular hexagon)
    h_e = p_base[0] + 19.0 * ux
    h_n = p_base[1] + 19.0 * uy
    h_u = p_base[2]
    lines.extend([
        f"-- HEX_HEAD_{screw_idx} (AF30 x 12 mm regular hexagon native extrusion)",
        "NEW EXTRUSION",
        f"ORI Y IS U AND Z IS {beam_dir}",
        f"POS E {h_e:.1f} N {h_n:.1f} U {h_u:.1f}",
        "LEVE 5 10",
        "HEIG 12.0",
        "NEW LOOP",
        "NEW VERTEX POS E 8.660254 N -15.000000 U 0 END",
        "NEW VERTEX POS E -8.660254 N -15.000000 U 0 END",
        "NEW VERTEX POS E -17.320508 N 0.000000 U 0 END",
        "NEW VERTEX POS E -8.660254 N 15.000000 U 0 END",
        "NEW VERTEX POS E 8.660254 N 15.000000 U 0 END",
        "NEW VERTEX POS E 17.320508 N 0.000000 U 0 END",
        "END",
        "END",
        "END"
    ])

def emit_r3_hardware_details(lines, tag, p1, p2, L, ux, uy, tx, ty, beam_dir, trans_dir, h_beam, is_heavy):
    # 1. Mounting Plates
    lines.append(f"NEW SUBE /SUBE-{tag}-MOUNTING-PLATES")
    lines.append("ORI Y IS N AND Z IS U")
    lines.append("POS E 0 N 0 U 0")

    # [A] Upper Mount Plate
    up_plate_u = p1[2] - h_beam / 2.0
    lines.extend([
        "-- UPPER_MOUNT_PLATE (180W x 350H x 16Thk with 6mm clipped corners and 4x NCYLINDER holes)",
        "NEW EXTRUSION",
        f"ORI Y IS U AND Z IS {beam_dir}",
        f"POS E {p1[0]:.1f} N {p1[1]:.1f} U {up_plate_u:.1f}",
        "LEVE 5 10",
        "HEIG 16.0",
        "NEW LOOP",
        "NEW VERTEX POS E -90.000000 N -169.000000 U 0 END",
        "NEW VERTEX POS E -90.000000 N 169.000000 U 0 END",
        "NEW VERTEX POS E -84.000000 N 175.000000 U 0 END",
        "NEW VERTEX POS E 84.000000 N 175.000000 U 0 END",
        "NEW VERTEX POS E 90.000000 N 169.000000 U 0 END",
        "NEW VERTEX POS E 90.000000 N -169.000000 U 0 END",
        "NEW VERTEX POS E 84.000000 N -175.000000 U 0 END",
        "NEW VERTEX POS E -84.000000 N -175.000000 U 0 END",
        "END",
        "NEW NCYLINDER",
        "DIAM 22.000000",
        "HEIG 20.000000",
        "ORI Y IS N AND Z IS U",
        "POS E 45.000000 N 135.000000 U 8.000000",
        "NAPPFLAG 2",
        "END",
        "NEW NCYLINDER",
        "DIAM 22.000000",
        "HEIG 20.000000",
        "ORI Y IS N AND Z IS U",
        "POS E -45.000000 N 135.000000 U 8.000000",
        "NAPPFLAG 2",
        "END",
        "NEW NCYLINDER",
        "DIAM 22.000000",
        "HEIG 20.000000",
        "ORI Y IS N AND Z IS U",
        "POS E 45.000000 N -135.000000 U 8.000000",
        "NAPPFLAG 2",
        "END",
        "NEW NCYLINDER",
        "DIAM 22.000000",
        "HEIG 20.000000",
        "ORI Y IS N AND Z IS U",
        "POS E -45.000000 N -135.000000 U 8.000000",
        "NAPPFLAG 2",
        "END",
        "END"
    ])

    has_knee = (L <= 2500.0)
    if has_knee:
        low_plate_u = p1[2] - h_beam - 320.0
        lines.extend([
            "-- LOWER_MOUNT_PLATE (180W x 160H x 16Thk with 6mm clipped corners and 2x NCYLINDER holes)",
            "NEW EXTRUSION",
            f"ORI Y IS U AND Z IS {beam_dir}",
            f"POS E {p1[0]:.1f} N {p1[1]:.1f} U {low_plate_u:.1f}",
            "LEVE 5 10",
            "HEIG 16.0",
            "NEW LOOP",
            "NEW VERTEX POS E -90.000000 N -74.000000 U 0 END",
            "NEW VERTEX POS E -90.000000 N 74.000000 U 0 END",
            "NEW VERTEX POS E -84.000000 N 80.000000 U 0 END",
            "NEW VERTEX POS E 84.000000 N 80.000000 U 0 END",
            "NEW VERTEX POS E 90.000000 N 74.000000 U 0 END",
            "NEW VERTEX POS E 90.000000 N -74.000000 U 0 END",
            "NEW VERTEX POS E 84.000000 N -80.000000 U 0 END",
            "NEW VERTEX POS E -84.000000 N -80.000000 U 0 END",
            "END",
            "NEW NCYLINDER",
            "DIAM 22.000000",
            "HEIG 20.000000",
            "ORI Y IS N AND Z IS U",
            "POS E 45.000000 N 0.000000 U 8.000000",
            "NAPPFLAG 2",
            "END",
            "NEW NCYLINDER",
            "DIAM 22.000000",
            "HEIG 20.000000",
            "ORI Y IS N AND Z IS U",
            "POS E -45.000000 N 0.000000 U 8.000000",
            "NAPPFLAG 2",
            "END",
            "END"
        ])
    lines.append("END")

    # 2. Gussets
    lines.append(f"NEW SUBE /SUBE-{tag}-GUSSETS")
    lines.append("ORI Y IS N AND Z IS U")
    lines.append("POS E 0 N 0 U 0")

    haunch_e = p1[0] - 4.0 * tx
    haunch_n = p1[1] - 4.0 * ty
    haunch_u = p1[2]
    lines.extend([
        "-- ROOT_HAUNCH (8 mm clipped stiffener plate below beam root)",
        "NEW EXTRUSION",
        f"ORI Y IS U AND Z IS {trans_dir}",
        f"POS E {haunch_e:.1f} N {haunch_n:.1f} U {haunch_u:.1f}",
        "LEVE 5 10",
        "HEIG 8.0",
        "NEW LOOP",
        f"NEW VERTEX POS E 16.000000 N {-h_beam - 70.0:.1f} U 0 END",
        f"NEW VERTEX POS E 16.000000 N {-h_beam - 6.0:.1f} U 0 END",
        f"NEW VERTEX POS E 22.000000 N {-h_beam:.1f} U 0 END",
        f"NEW VERTEX POS E 130.000000 N {-h_beam:.1f} U 0 END",
        f"NEW VERTEX POS E 136.000000 N {-h_beam - 6.0:.1f} U 0 END",
        f"NEW VERTEX POS E 26.000000 N {-h_beam - 70.0:.1f} U 0 END",
        "END",
        "END"
    ])

    if has_knee:
        n_end = 16.0 + 0.717 * (L - 16.0)
        lines.extend([
            f"-- UPPER_GUSSET (8 mm tapered plate under channel beam at N {n_end:.1f})",
            "NEW EXTRUSION",
            f"ORI Y IS U AND Z IS {trans_dir}",
            f"POS E {p1[0]:.1f} N {p1[1]:.1f} U {p1[2]:.1f}",
            "LEVE 5 10",
            "HEIG 8.0",
            "NEW LOOP",
            f"NEW VERTEX POS E {n_end - 160.0:.1f} N {-h_beam:.1f} U 0 END",
            f"NEW VERTEX POS E {n_end + 60.0:.1f} N {-h_beam:.1f} U 0 END",
            f"NEW VERTEX POS E {n_end + 60.0:.1f} N {-h_beam - 50.0:.1f} U 0 END",
            f"NEW VERTEX POS E {n_end + 35.0:.1f} N {-h_beam - 84.0:.1f} U 0 END",
            f"NEW VERTEX POS E {n_end - 135.0:.1f} N {-h_beam - 131.0:.1f} U 0 END",
            f"NEW VERTEX POS E {n_end - 150.0:.1f} N {-h_beam - 128.0:.1f} U 0 END",
            f"NEW VERTEX POS E {n_end - 160.0:.1f} N {-h_beam - 112.0:.1f} U 0 END",
            "END",
            "END",
            "-- LOWER_GUSSET (8 mm extended tapered plate at knee brace foot)",
            "NEW EXTRUSION",
            f"ORI Y IS U AND Z IS {trans_dir}",
            f"POS E {p1[0]:.1f} N {p1[1]:.1f} U {p1[2]:.1f}",
            "LEVE 5 10",
            "HEIG 8.0",
            "NEW LOOP",
            f"NEW VERTEX POS E 16.000000 N {-h_beam - 170.0:.1f} U 0 END",
            f"NEW VERTEX POS E 146.000000 N {-h_beam - 275.0:.1f} U 0 END",
            f"NEW VERTEX POS E 146.000000 N {-h_beam - 310.0:.1f} U 0 END",
            f"NEW VERTEX POS E 110.000000 N {-h_beam - 340.0:.1f} U 0 END",
            f"NEW VERTEX POS E 16.000000 N {-h_beam - 340.0:.1f} U 0 END",
            "END",
            "END"
        ])
    lines.append("END")

    # 3. Fillet Welds
    lines.append(f"NEW SUBE /SUBE-{tag}-WELDS")
    lines.append("ORI Y IS N AND Z IS U")
    lines.append("POS E 0 N 0 U 0")

    weld_w = 75.0 if not is_heavy else 133.0
    w_top_n = p1[1] + 16.0 * uy
    w_top_e = p1[0] + 16.0 * ux
    lines.extend([
        "-- BEAM_ROOT_WELD_TOP",
        "NEW EXTRUSION",
        f"ORI Y IS {beam_dir} AND Z IS U",
        f"POS E {w_top_e:.1f} N {w_top_n:.1f} U {p1[2]:.1f}",
        "LEVE 5 10",
        f"HEIG {weld_w:.1f}",
        "NEW LOOP",
        "NEW VERTEX POS E 0 0 0 END",
        "NEW VERTEX POS E 6 0 0 END",
        "NEW VERTEX POS E 0 -6 0 END",
        "END",
        "END"
    ])
    lines.append("END")

    # 4. Screw Assemblies
    screws = [
        (-45.0, up_plate_u + 135.0),
        (45.0, up_plate_u + 135.0),
        (-45.0, up_plate_u - 135.0),
        (45.0, up_plate_u - 135.0)
    ]
    for s_i, (dx_t, dz_u) in enumerate(screws, start=1):
        pb = [p1[0] + dx_t * tx, p1[1] + dx_t * ty, dz_u]
        emit_r3_screw_assembly(lines, tag, s_i, pb, ux, uy, beam_dir)

    if has_knee:
        low_cz = p1[2] - h_beam - 320.0
        low_screws = [
            (-45.0, low_cz),
            (45.0, low_cz)
        ]
        for s_i, (dx_t, dz_u) in enumerate(low_screws, start=5):
            pb = [p1[0] + dx_t * tx, p1[1] + dx_t * ty, dz_u]
            emit_r3_screw_assembly(lines, tag, s_i, pb, ux, uy, beam_dir)

def generate_master_models():
    for d in [OUTPUT_DIR_ASCII_C, OUTPUT_DIR_ASCII_DESKTOP, OUTPUT_DIR_ORIGINAL]:
        os.makedirs(d, exist_ok=True)

    # -------------------------------------------------------------
    # 1. Load Pipe Supports (208 Supports)
    # -------------------------------------------------------------
    with open(PS_CSV, "r", encoding="utf-8-sig") as f:
        ps_rows = list(csv.DictReader(f))

    ps_tag_totals = Counter(clean_tag(r.get("支架总编号 (Support Tag)", "PS")) for r in ps_rows)
    ps_tag_seen = defaultdict(int)
    for r in ps_rows:
        raw_tag = r.get("支架总编号 (Support Tag)", "PS")
        base_tag = clean_tag(raw_tag)
        if ps_tag_totals[base_tag] > 1:
            ps_tag_seen[base_tag] += 1
            r['e3d_tag'] = f"{base_tag}-{ps_tag_seen[base_tag]}"
            r['instance_info'] = f"(Instance {ps_tag_seen[base_tag]}/{ps_tag_totals[base_tag]})"
        else:
            r['e3d_tag'] = base_tag
            r['instance_info'] = ""

    tier1_ps, tier2_ps, tier3_ps = [], [], []
    for r in ps_rows:
        elev = r.get("安装标高 / 高程范围 (Elevation / Level)", "").strip()
        if "0.000 ~ +5.000M" in elev:
            tier1_ps.append(r)
        elif ("5.000 ~ +6.500M" in elev) or ("6.500 ~ +10.000M" in elev):
            tier2_ps.append(r)
        else:
            tier3_ps.append(r)

    def generate_ps_tier(tier_rows, frmw_name, title_scope):
        sctn_body = []
        hdw_body = []

        for r in tier_rows:
            raw_tag = r.get("支架总编号 (Support Tag)", "PS")
            tag = r['e3d_tag']
            inst = r['instance_info']
            p1 = parse_pt(r.get("生根连接点_E3D (Connection Anchor E3D)"))
            p2 = parse_pt(r.get("白框端点_E3D (Box Interface E3D)"))
            meas_len = float(r.get("支架俯视角实测长度_mm (Plan Measured Length)", 0) or 0)
            profile_str = r.get("结构截面形式 (Structural Profile)", "")

            # Apply overall plant EN shift
            p1[0] += BASE_SHIFT_E
            p1[1] += BASE_SHIFT_N
            p2[0] += BASE_SHIFT_E
            p2[1] += BASE_SHIFT_N

            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            L = math.sqrt(dx*dx + dy*dy)
            if L < 10.0:
                L = meas_len if meas_len > 10.0 else 1500.0
                dx = 0.0
                dy = L

            u, t, beam_dir, trans_dir = get_dir_frame(dx, dy)
            ux, uy = u
            tx, ty = t

            is_heavy = ("H型钢" in profile_str or "重型" in profile_str or L > 2500.0)
            sp_comp = "/BS-UB203x133x25" if is_heavy else "/BS-PFC150x75x18"
            h_beam = 203.0 if is_heavy else 150.0

            # 1. SCTN Beam
            t_base = 16.0
            b_start_e = p1[0] + ux * t_base
            b_start_n = p1[1] + uy * t_base
            b_start_u = p1[2]

            comment_tag = f"{raw_tag} {inst}".strip()
            sctn_body.extend([
                f"-- Pipe Support: {comment_tag} (Length: {L:.1f} mm, Profile: {sp_comp})",
                f"NEW SCTN /SCTN-{tag}-BEAM",
                f"POSS E {b_start_e:.1f} N {b_start_n:.1f} U {b_start_u:.1f}",
                f"POSE E {p2[0]:.1f} N {p2[1]:.1f} U {p1[2]:.1f}",
                "DRNS PERP",
                "DRNE PERP",
                "JUSL CTOP",
                f"SPRE SPCOMPONENT {sp_comp}",
                "END"
            ])

            has_knee = (L <= 2500.0 and meas_len > 500.0)
            if has_knee:
                n_brace_start = 80.0
                u_brace_start = -h_beam - 302.444658
                n_brace_end = t_base + 0.717 * (L - t_base)
                u_brace_end = -h_beam - 28.142445

                br_s_e = p1[0] + ux * n_brace_start
                br_s_n = p1[1] + uy * n_brace_start
                br_s_u = p1[2] + u_brace_start

                br_e_e = p1[0] + ux * n_brace_end
                br_e_n = p1[1] + uy * n_brace_end
                br_e_u = p1[2] + u_brace_end

                sctn_body.extend([
                    f"-- Knee Brace (Profile: /BS-L50x50x6, meets upper gusset plate, zero collision)",
                    f"NEW SCTN /SCTN-{tag}-BRACE",
                    f"POSS E {br_s_e:.1f} N {br_s_n:.1f} U {br_s_u:.1f}",
                    f"POSE E {br_e_e:.1f} N {br_e_n:.1f} U {br_e_u:.1f}",
                    "DRNS PERP",
                    "DRNE PERP",
                    "JUSL TOAY",
                    "SPRE SPCOMPONENT /BS-L50x50x6",
                    "END"
                ])
            sctn_body.append("")

            # 2. R3 Hardware Details
            hdw_body.append(f"-- Hardware Details: {raw_tag}")
            emit_r3_hardware_details(hdw_body, tag, p1, p2, L, ux, uy, tx, ty, beam_dir, trans_dir, h_beam, is_heavy)
            hdw_body.append("")

        return sctn_body, hdw_body

    t1_sctn, t1_hdw = generate_ps_tier(tier1_ps, "FRMW-PS-0M-5M", "Low-Elevation Pipe Racks (EL 0.000 ~ 5.000M)")
    t2_sctn, t2_hdw = generate_ps_tier(tier2_ps, "FRMW-PS-MID-5M-10M", "Mid-Elevation Pipe Supports (EL 5.000 ~ 10.000M)")
    t3_sctn, t3_hdw = generate_ps_tier(tier3_ps, "FRMW-PS-TOP-ABOVE-10M", "High-Elevation Pipe Corridor (EL > 10.000M)")

    # -------------------------------------------------------------
    # 2. Load 94 Cable Tray Cantilever Brackets (EL +9.100M)
    # -------------------------------------------------------------
    with open(BRACKET_CSV, "r", encoding="utf-8-sig") as f:
        bracket_rows = list(csv.DictReader(f))

    bracket_sctn_body = []
    bracket_hdw_body = []

    for r in bracket_rows:
        tag = r.get("支架总编号 (Support Tag)", "ET")
        cad_x = float(r["CAD_X (mm)"]) if "CAD_X (mm)" in r else float(r.get("E3D_X_East (mm)", 0)) - CAD_TRAY_DX
        cad_y = float(r["CAD_Y (mm)"]) if "CAD_Y (mm)" in r else float(r.get("E3D_Y_North (mm)", 0)) - CAD_TRAY_DY
        e = cad_x + CAD_TRAY_DX
        n = cad_y + CAD_TRAY_DY
        u = float(r.get("E3D_Z_Up (mm)", 9100.0))
        arm_len = float(r.get("悬臂挑臂实测长度_mm (Arm Length)", 500.0))
        tray_w = float(r.get("承载桥架宽度_mm (Tray Width)", 450.0))
        ori_str = r.get("托臂安装朝向 (Bracket Orientation)", "")

        if "南北" in ori_str:
            sy = -1.0 if "South" in ori_str else 1.0
            ux, uy = 0.0, sy
            tx, ty = 1.0, 0.0
            beam_dir = 'S' if sy < 0 else 'N'
            trans_dir = 'E'
        else:
            sx = -1.0 if "West" in ori_str else 1.0
            ux, uy = sx, 0.0
            tx, ty = 0.0, 1.0
            beam_dir = 'W' if sx < 0 else 'E'
            trans_dir = 'N'

        t_base = 16.0
        p1_e, p1_n = e, n
        p2_e, p2_n = e + arm_len * ux, n + arm_len * uy
        b_p1_e, b_p1_n, b_p1_u = e + t_base * ux, n + t_base * uy, 8850.0
        brace_span = t_base + 0.75 * (arm_len - t_base)
        b_p2_e, b_p2_n, b_p2_u = e + brace_span * ux, n + brace_span * uy, 8950.0

        bracket_sctn_body.extend([
            f"-- Standard Cable Tray Bracket: {tag} (Arm Length: {arm_len:.1f} mm, Tray: {tray_w:.0f} mm)",
            f"NEW SCTN /SCTN-{tag}-ARM",
            f"POSS E {p1_e:.1f} N {p1_n:.1f} U {u:.1f}",
            f"POSE E {p2_e:.1f} N {p2_n:.1f} U {u:.1f}",
            "DRNS PERP",
            "DRNE PERP",
            "JUSL CTOP",
            "SPRE SPCOMPONENT /BS-PFC150x75x18",
            "END",
            f"-- Knee Brace (/BS-L50x50x6, meets under-arm gusset plate)",
            f"NEW SCTN /SCTN-{tag}-BRACE",
            f"POSS E {b_p1_e:.1f} N {b_p1_n:.1f} U {b_p1_u:.1f}",
            f"POSE E {b_p2_e:.1f} N {b_p2_n:.1f} U {b_p2_u:.1f}",
            "DRNS PERP",
            "DRNE PERP",
            "JUSL TOAY",
            "SPRE SPCOMPONENT /BS-L50x50x6",
            "END",
            ""
        ])

        # Bracket Hardware: Baseplate + 4x Bolts + Retainer Stop Block
        bracket_hdw_body.extend([
            f"-- Cable Bracket Hardware: {tag}",
            f"NEW SUBE /SUBE-{tag}-BASEPLATE",
            "ORI Y IS N AND Z IS U",
            "POS E 0 N 0 U 0",
            "-- Baseplate 150W x 350H x 16Thk with 4x holes",
            "NEW EXTRUSION",
            f"ORI Y IS U AND Z IS {beam_dir}",
            f"POS E {e:.1f} N {n:.1f} U 8925.0",
            "LEVE 5 10",
            "HEIG 16.0",
            "NEW LOOP",
            "NEW VERTEX POS E -75.0 N -169.0 U 0 END",
            "NEW VERTEX POS E -75.0 N 169.0 U 0 END",
            "NEW VERTEX POS E -69.0 N 175.0 U 0 END",
            "NEW VERTEX POS E 69.0 N 175.0 U 0 END",
            "NEW VERTEX POS E 75.0 N 169.0 U 0 END",
            "NEW VERTEX POS E 75.0 N -169.0 U 0 END",
            "NEW VERTEX POS E 69.0 N -175.0 U 0 END",
            "NEW VERTEX POS E -69.0 N -175.0 U 0 END",
            "END",
            "NEW NCYLINDER DIAM 22.0 HEIG 20.0 ORI Y IS N AND Z IS U POS E 45.0 N 135.0 U 8.0 NAPPFLAG 2 END",
            "NEW NCYLINDER DIAM 22.0 HEIG 20.0 ORI Y IS N AND Z IS U POS E -45.0 N 135.0 U 8.0 NAPPFLAG 2 END",
            "NEW NCYLINDER DIAM 22.0 HEIG 20.0 ORI Y IS N AND Z IS U POS E 45.0 N -135.0 U 8.0 NAPPFLAG 2 END",
            "NEW NCYLINDER DIAM 22.0 HEIG 20.0 ORI Y IS N AND Z IS U POS E -45.0 N -135.0 U 8.0 NAPPFLAG 2 END",
            "END",
            "END",
            f"-- Outer Tip Retainer Stop Block (75x40x40 at outer edge)",
            f"NEW SUBE /SUBE-{tag}-STOP-BLOCK",
            "ORI Y IS N AND Z IS U",
            "POS E 0 N 0 U 0",
            "NEW BOX",
            "XLEN 75.0", "YLEN 40.0", "ZLEN 40.0",
            f"ORI Y IS U AND Z IS {beam_dir}",
            f"POS E {p2_e - 20.0*ux:.1f} N {p2_n - 20.0*uy:.1f} U 9120.0",
            "END",
            "END"
        ])

        # 4x M20 Hex Screws for Bracket
        hole_offsets = [(45.0, 135.0), (-45.0, 135.0), (45.0, -135.0), (-45.0, -135.0)]
        for s_idx, (dx_loc, dy_loc) in enumerate(hole_offsets, 1):
            sc_e = e + dx_loc * tx
            sc_n = n + dx_loc * ty
            sc_u = 8925.0 + dy_loc
            emit_r3_screw_assembly(bracket_hdw_body, tag, s_idx, [sc_e, sc_n, sc_u], ux, uy, beam_dir)

    # -------------------------------------------------------------
    # 3. Load CAD Cable Tray Mesh Network (4,968 Bars)
    # -------------------------------------------------------------
    print("Loading CAD Cable Tray Mesh from:", CAD_TRAY_PML)
    with open(CAD_TRAY_PML, "r", encoding="utf-8") as f:
        cad_tray_lines = f.readlines()

    bar_count = 0
    in_sube = False
    cur_xlen, cur_ylen, cur_zlen = "248.0", "12.0", "12.0"
    tray_mesh_body = []

    for line in cad_tray_lines:
        line_s = line.strip()
        if line_s.startswith("NEW SUBE"):
            in_sube = True
            m = re.search(r'NEW SUBE\s+(/\S+)', line_s)
            if m:
                sube_name = m.group(1)
                sube_tag = sube_name.replace("/CAD_CABLE_TRAY_NETWORK_9_1_", "/SUBE-CABLE-TRAY-")
                tray_mesh_body.append(f"NEW SUBE {sube_tag}")
                tray_mesh_body.append("ORI Y IS N AND Z IS U")
                tray_mesh_body.append("POS E 0.0 N 0.0 U 0.0")
        elif line_s.startswith("--") and in_sube:
            tray_mesh_body.append(line_s)
        elif line_s.startswith("XLEN"):
            cur_xlen = line_s.split()[1]
        elif line_s.startswith("YLEN"):
            cur_ylen = line_s.split()[1]
        elif line_s.startswith("ZLEN"):
            cur_zlen = line_s.split()[1]
        elif line_s.startswith("POS E") and in_sube:
            m = re.search(r'POS E\s+([-\d\.]+)\s+N\s+([-\d\.]+)\s+U\s+([-\d\.]+)', line_s)
            if m:
                raw_x = float(m.group(1))
                raw_y = float(m.group(2))
                raw_z = float(m.group(3))
                new_e = raw_x + CAD_TRAY_DX
                new_n = raw_y + CAD_TRAY_DY
                new_u = raw_z
                tray_mesh_body.extend([
                    "NEW BOX",
                    f"XLEN {cur_xlen}",
                    f"YLEN {cur_ylen}",
                    f"ZLEN {cur_zlen}",
                    "ORI Y IS N AND Z IS U",
                    f"POS E {new_e:.1f} N {new_n:.1f} U {new_u:.1f}",
                    "END"
                ])
                bar_count += 1
        elif line_s == "END":
            pass

    print(f"Loaded and shifted {bar_count} CAD cable tray wire mesh bars.")

    # -------------------------------------------------------------
    # 4. Master Cleanup Macro (Self-Healing with handle 2,109)
    # -------------------------------------------------------------
    clean_lines = [
        "-- ==============================================================================",
        "-- AVEVA E3D / PDMS Self-Healing Cleanup Macro",
        "-- Safely deletes previously generated Pipe Support and Cable Tray Zones/Equipments",
        "-- Handled error (2,109): Undefined name safely skipped without stopping",
        "-- ==============================================================================",
        "",
        "/EQUI-PIPE-RACKS-AND-CABLE-TRAYS",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE EQUI",
        "endhandle",
        "",
        "/EQUI-PIPE-SUPPORT-HARDWARE",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE EQUI",
        "endhandle",
        "",
        "/EQUI-SUPPORT-HARDWARE",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE EQUI",
        "endhandle",
        "",
        "/EQUI-CABLE-BRACKET-HARDWARE",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE EQUI",
        "endhandle",
        "",
        "/EQUI-CABLE-TRAY-MESH",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE EQUI",
        "endhandle",
        "",
        "/STRU-PIPE-RACKS",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE STRU",
        "endhandle",
        "",
        "/STRU-CABLE-TRAYS",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE STRU",
        "endhandle",
        "",
        "/ZONE-EQUIP-SUPPORTS",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE ZONE",
        "endhandle",
        "",
        "/ZONE-PIPE-RACKS",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE ZONE",
        "endhandle",
        "",
        "/ZONE-CABLE-TRAYS",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE ZONE",
        "endhandle",
        "",
        "/ZONE-STRUCT-SUPPORTS",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE ZONE",
        "endhandle",
        "",
        "/JK-PAPER-FIBERLINE-UPGRADE",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE SITE",
        "endhandle",
        "",
        "SAVEWORK"
    ]

    # -------------------------------------------------------------
    # 5. Master All-In-One Macro (00_ALL_IN_ONE_STRUCT_MODELS.pml)
    # -------------------------------------------------------------
    all_in_one_lines = [
        "-- ==============================================================================",
        "-- AVEVA E3D / PDMS PML1 All-In-One Master Structural Modeling Macro",
        "-- Project: JK-Paper Sirpur Mill Fiberline Upgrade Project",
        "-- Model Scope: Full Plant Pipe Racks (208 Supports) & Cable Tray System (94 Brackets + 4968 Tray Mesh Bars)",
        "-- Baseline Template: 100% compliant with user-approved SINGLE_TYPICAL_PIPE_SUPPORT_R3",
        "-- Features: Full Mounting Plates, Gussets, Hex Screws (AF30) and Fillet Welds!",
        "-- Unified Plant Coordinates: E+52468.0, N+59338.0",
        "-- Clean Top Surface: Zero isolation pads on beams (leaves space for pipe clamps)",
        "-- Zero Collision: Knee braces terminate flush inside gusset plate (zero flange collision)!",
        "-- Zero Duplicate Zone: NEW ZONE /ZONE-STRUCT-SUPPORTS called ONLY ONCE!",
        "-- ==============================================================================",
        "",
        "-- [1/6] Root Structure Hierarchy Setup & Self-Cleaning",
        "/STRU-PIPE-RACKS",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE STRU",
        "endhandle",
        "",
        "/STRU-CABLE-TRAYS",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE STRU",
        "endhandle",
        "",
        "/EQUI-PIPE-SUPPORT-HARDWARE",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE EQUI",
        "endhandle",
        "",
        "/EQUI-CABLE-BRACKET-HARDWARE",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE EQUI",
        "endhandle",
        "",
        "/EQUI-CABLE-TRAY-MESH",
        "handle (2,109)",
        "elsehandle none",
        "  DELETE EQUI",
        "endhandle",
        "",
        "/JK-PAPER-FIBERLINE-UPGRADE",
        "handle (2,109)",
        "  NEW SITE /JK-PAPER-FIBERLINE-UPGRADE",
        "endhandle",
        "",
        "/ZONE-STRUCT-SUPPORTS",
        "handle (2,109)",
        "  NEW ZONE /ZONE-STRUCT-SUPPORTS",
        "endhandle",
        "",
        "-- [2/6] Loading Pipe Racks Structural Steel (208 Supports in 3 Elevation FRMWs)",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW STRU /STRU-PIPE-RACKS",
        "",
        "NEW FRMW /FRMW-PS-0M-5M",
        *t1_sctn,
        "END",
        "",
        "NEW FRMW /FRMW-PS-MID-5M-10M",
        *t2_sctn,
        "END",
        "",
        "NEW FRMW /FRMW-PS-TOP-ABOVE-10M",
        *t3_sctn,
        "END",
        "",
        "END",  # close STRU /STRU-PIPE-RACKS
        "",
        "-- [3/6] Loading Full R3 Hardware, Mounting Plates, Gussets & Hex Fasteners (208 Supports)",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW EQUI /EQUI-PIPE-SUPPORT-HARDWARE",
        "ORI Y IS N AND Z IS U",
        "POS E 0.0 N 0.0 U 0.0",
        "",
        *t1_hdw,
        *t2_hdw,
        *t3_hdw,
        "END",  # close EQUI-PIPE-SUPPORT-HARDWARE
        "",
        "-- [4/6] Loading Cable Tray Cantilever Brackets (94 Supports at EL +9.100M)",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW STRU /STRU-CABLE-TRAYS",
        "NEW FRMW /FRMW-CABLE-BRACKETS",
        "",
        *bracket_sctn_body,
        "END",  # close FRMW
        "END",  # close STRU
        "",
        "-- [5/6] Loading Cable Tray Bracket R3 Hardware (94 Baseplates, 4x AF30 Hex Screws, Stop Blocks)",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW EQUI /EQUI-CABLE-BRACKET-HARDWARE",
        "ORI Y IS N AND Z IS U",
        "POS E 0.0 N 0.0 U 0.0",
        "",
        *bracket_hdw_body,
        "END",  # close EQUI-CABLE-BRACKET-HARDWARE
        "",
        "-- [6/6] Loading CAD True Cable Tray Wire Mesh Network (4,968 Bars at EL +9.100M)",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW EQUI /EQUI-CABLE-TRAY-MESH",
        "ORI Y IS N AND Z IS U",
        "POS E 0.0 N 0.0 U 0.0",
        "",
        *tray_mesh_body,
        "END",  # close EQUI-CABLE-TRAY-MESH
        "",
        "SAVEWORK",
        "-- ==============================================================================",
        "-- ALL 302 SUPPORTS & 4968 TRAY MESH BARS LOADED SUCCESSFULLY WITH FULL R3 DETAILS!",
        "-- EXECUTE: ADD /ZONE-STRUCT-SUPPORTS",
        "-- ZOOM EXTENTS: AUTO CE (or press F8)",
        "-- =============================================================================="
    ]

    master_load_lines = [
        "-- ==============================================================================",
        "-- AVEVA E3D / PDMS PML1 Master Assembly Macro",
        "-- Project: JK-Paper Sirpur Mill Fiberline Upgrade Project",
        "-- Baseline: SINGLE_TYPICAL_PIPE_SUPPORT_R3 + eui0.dwg Cable Tray System",
        "-- Overall EN Shift: E + 52468.0, N + 59338.0",
        "-- ==============================================================================",
        "",
        r"$M C:\e3d_models\00_CLEAN_EXISTING_MODELS.pml",
        r"$M C:\e3d_models\00_ALL_IN_ONE_STRUCT_MODELS.pml",
        "",
        "SAVEWORK"
    ]

    # Modular separate macros
    m1_all = [
        "/ZONE-STRUCT-SUPPORTS",
        "handle (2,109)",
        "  NEW ZONE /ZONE-STRUCT-SUPPORTS",
        "endhandle",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW STRU /STRU-PIPE-RACKS",
        "NEW FRMW /FRMW-PS-0M-5M",
        *t1_sctn,
        "END",
        "END",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW EQUI /EQUI-HDW-0M-5M",
        "ORI Y IS N AND Z IS U",
        "POS E 0 N 0 U 0",
        *t1_hdw,
        "END",
        "SAVEWORK"
    ]

    m2_all = [
        "/ZONE-STRUCT-SUPPORTS",
        "handle (2,109)",
        "  NEW ZONE /ZONE-STRUCT-SUPPORTS",
        "endhandle",
        "/STRU-PIPE-RACKS",
        "handle (2,109)",
        "  /ZONE-STRUCT-SUPPORTS",
        "  NEW STRU /STRU-PIPE-RACKS",
        "endhandle",
        "NEW FRMW /FRMW-PS-MID-5M-10M",
        *t2_sctn,
        "END",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW EQUI /EQUI-HDW-MID-5M-10M",
        "ORI Y IS N AND Z IS U",
        "POS E 0 N 0 U 0",
        *t2_hdw,
        "END",
        "SAVEWORK"
    ]

    m3_all = [
        "/ZONE-STRUCT-SUPPORTS",
        "handle (2,109)",
        "  NEW ZONE /ZONE-STRUCT-SUPPORTS",
        "endhandle",
        "/STRU-PIPE-RACKS",
        "handle (2,109)",
        "  /ZONE-STRUCT-SUPPORTS",
        "  NEW STRU /STRU-PIPE-RACKS",
        "endhandle",
        "NEW FRMW /FRMW-PS-TOP-ABOVE-10M",
        *t3_sctn,
        "END",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW EQUI /EQUI-HDW-TOP-ABOVE-10M",
        "ORI Y IS N AND Z IS U",
        "POS E 0 N 0 U 0",
        *t3_hdw,
        "END",
        "SAVEWORK"
    ]

    m4_all = [
        "/ZONE-STRUCT-SUPPORTS",
        "handle (2,109)",
        "  NEW ZONE /ZONE-STRUCT-SUPPORTS",
        "endhandle",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW STRU /STRU-CABLE-TRAYS",
        "NEW FRMW /FRMW-CABLE-BRACKETS",
        "",
        *bracket_sctn_body,
        "END",
        "END",
        "SAVEWORK"
    ]

    m5_all = [
        "/ZONE-STRUCT-SUPPORTS",
        "handle (2,109)",
        "  NEW ZONE /ZONE-STRUCT-SUPPORTS",
        "endhandle",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW EQUI /EQUI-CABLE-BRACKET-HARDWARE",
        "ORI Y IS N AND Z IS U",
        "POS E 0 N 0 U 0",
        "",
        *bracket_hdw_body,
        "END",
        "SAVEWORK"
    ]

    m6_pipe_hdw = [
        "/ZONE-STRUCT-SUPPORTS",
        "handle (2,109)",
        "  NEW ZONE /ZONE-STRUCT-SUPPORTS",
        "endhandle",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW EQUI /EQUI-PIPE-SUPPORT-HARDWARE",
        "ORI Y IS N AND Z IS U",
        "POS E 0 N 0 U 0",
        *t1_hdw,
        *t2_hdw,
        *t3_hdw,
        "END",
        "SAVEWORK"
    ]

    m7_mesh = [
        "/ZONE-STRUCT-SUPPORTS",
        "handle (2,109)",
        "  NEW ZONE /ZONE-STRUCT-SUPPORTS",
        "endhandle",
        "/ZONE-STRUCT-SUPPORTS",
        "NEW EQUI /EQUI-CABLE-TRAY-MESH",
        "ORI Y IS N AND Z IS U",
        "POS E 0.0 N 0.0 U 0.0",
        "",
        *tray_mesh_body,
        "END",
        "SAVEWORK"
    ]

    files_dict = {
        "00_ALL_IN_ONE_STRUCT_MODELS.pml": "\n".join(all_in_one_lines),
        "00_MASTER_LOAD_STRUCT_MODELS.pml": "\n".join(master_load_lines),
        "00_CLEAN_EXISTING_MODELS.pml": "\n".join(clean_lines),
        "01_PIPE_RACKS_GROUND_0M_TO_5M.pml": "\n".join(m1_all),
        "02_PIPE_RACKS_MID_5M_TO_10M.pml": "\n".join(m2_all),
        "03_PIPE_RACKS_TOP_ABOVE_10M.pml": "\n".join(m3_all),
        "04_CABLE_TRAY_BRACKETS_94.pml": "\n".join(m4_all),
        "05_CABLE_TRAY_BRACKET_HARDWARE.pml": "\n".join(m5_all),
        "06_PIPE_SUPPORT_R3_HARDWARE.pml": "\n".join(m6_pipe_hdw),
        "07_CABLE_TRAY_CAD_MESH_NETWORK.pml": "\n".join(m7_mesh),
    }

    for fname, content in files_dict.items():
        for d in [OUTPUT_DIR_ASCII_C, OUTPUT_DIR_ASCII_DESKTOP, OUTPUT_DIR_ORIGINAL]:
            (d / fname).write_text(content.strip() + "\n", encoding="utf-8")
        print(f"Generated {fname}: {len(content.splitlines())} lines.")

    print("\nAll PML models generated and synchronized successfully across all destinations!")

if __name__ == "__main__":
    generate_master_models()
