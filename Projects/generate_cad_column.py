# -*- coding: utf-8 -*-
"""
Reconstruct Column / Vessel 3D PML model from CAD 2D lines.
Axis is East-West (X).
Centerline Y (North) = 76361.4130 mm.
Assuming elevation U = 0 (or standard baseline).
"""

# Segments from East to West:
# 1. CYLINDER (East end):
#    E in [73864.5157, 73977.7233], Length = 113.2076 mm, Diam = 274.9326 mm
#    Center E = 73921.1195 mm
# 2. CONE (Transition 1):
#    E in [73837.5616, 73864.5157], Length = 26.9541 mm
#    East Diam (DTOP) = 274.9326 mm, West Diam (DBOT) = 296.4960 mm
#    Center E = 73851.0387 mm
# 3. CYLINDER (Collar/Flange):
#    E in [73783.6532, 73837.5616], Length = 53.9084 mm, Diam = 393.5311 mm
#    Center E = 73810.6074 mm
# 4. CONE (Transition 2):
#    E in [73762.0898, 73783.6532], Length = 21.5634 mm
#    East Diam (DBOT) = 296.4960 mm, West Diam (DTOP) = 274.9326 mm
#    Center E = 73772.8715 mm
# 5. CYLINDER (Main body):
#    E in [73497.9389, 73762.0898], Length = 264.1509 mm, Diam = 274.9326 mm
#    Center E = 73630.0144 mm
# 6. CONE (West reducer):
#    E in [73390.1221, 73497.9389], Length = 107.8168 mm
#    East Diam (DBOT) = 274.9326 mm, West Diam (DTOP) = 221.0242 mm
#    Center E = 73444.0305 mm

def generate_column_pml(equi_name="/CAD_AID_LOOSE_001", center_u=0.0):
    n_val = 76361.41
    u_val = center_u
    
    # In E3D PML1:
    # A horizontal cylinder/cone along East-West:
    # Axis along East: ORI Y is U and Z is E  (or ORI Y is N and Z is E)
    # Height is along local Z (which points to E).
    # For a CYLINDER with ORI Y is U and Z is E:
    # POS is geometric center (E, N, U).
    # DIAM is diameter.
    # HEIG is length along Z (E).
    #
    # For a CONE with ORI Y is U and Z is E:
    # POS is geometric center (E, N, U).
    # DBOT is diameter at -Z (West end), DTOP is diameter at +Z (East end).
    # HEIG is length along Z (E).
    
    lines = [
        "$S-  -- Synonym translation OFF",
        "-- ----------------------------------------------------------------",
        f"-- Equipment Listing: {equi_name}",
        "-- Assembly: East-West Horizontal Column / Vessel from CAD JSON",
        "",
        "ONERROR GOLABEL /ERROR3",
        "",
        "INPUT BEGIN",
        f"NEW EQUIPMENT {equi_name}",
        "DESC 'HORIZONTAL COLUMN ASSEMBLY'",
        "BUIL false",
        "DSCO unset",
        "PTSP unset",
        "INSC unset",
        "",
        f"NEW SUBEQUIPMENT {equi_name}_BODY",
        "BUIL false",
        "DSCO unset",
        "PTSP unset",
        "INSC unset",
        "",
        "-- Segment 1: East Cylinder (DN275 class)",
        "NEW CYLINDER",
        f"POS E 73921.12mm N {n_val:.2f}mm U {u_val:.2f}mm",
        "ORI Y is U and Z is E",
        "DIAM 274.93mm",
        "HEIG 113.21mm",
        "END",
        "",
        "-- Segment 2: Transition Cone (274.93 -> 296.50)",
        "NEW CONE",
        f"POS E 73851.04mm N {n_val:.2f}mm U {u_val:.2f}mm",
        "ORI Y is U and Z is E",
        "DTOP 274.93mm",
        "DBOT 296.50mm",
        "HEIG 26.95mm",
        "END",
        "",
        "-- Segment 3: Collar / Flange Ring (OD 393.53)",
        "NEW CYLINDER",
        f"POS E 73810.61mm N {n_val:.2f}mm U {u_val:.2f}mm",
        "ORI Y is U and Z is E",
        "DIAM 393.53mm",
        "HEIG 53.91mm",
        "END",
        "",
        "-- Segment 4: Transition Cone (296.50 -> 274.93)",
        "NEW CONE",
        f"POS E 73772.87mm N {n_val:.2f}mm U {u_val:.2f}mm",
        "ORI Y is U and Z is E",
        "DTOP 296.50mm",
        "DBOT 274.93mm",
        "HEIG 21.56mm",
        "END",
        "",
        "-- Segment 5: Main Body Cylinder (DN275 class)",
        "NEW CYLINDER",
        f"POS E 73630.01mm N {n_val:.2f}mm U {u_val:.2f}mm",
        "ORI Y is U and Z is E",
        "DIAM 274.93mm",
        "HEIG 264.15mm",
        "END",
        "",
        "-- Segment 6: West Reducer Cone (274.93 -> 221.02)",
        "NEW CONE",
        f"POS E 73444.03mm N {n_val:.2f}mm U {u_val:.2f}mm",
        "ORI Y is U and Z is E",
        "DTOP 274.93mm",
        "DBOT 221.02mm",
        "HEIG 107.82mm",
        "END",
        "",
        "END",
        f"INPUT END  EQUIPMENT {equi_name}",
        "INPUT FINISH",
        "LABEL /ERROR3",
        "handle ANY",
        "$S+",
        "RETURN ERROR",
        "endhandle",
        "$S+",
        "-- ----------------------------------------------------------------"
    ]
    return "\n".join(lines)

pml_text = generate_column_pml()
print("Generated PML:")
print(pml_text)

with open("Projects/CAD_AID_LOOSE_001.pml", "w", encoding="utf-8") as f:
    f.write(pml_text)
