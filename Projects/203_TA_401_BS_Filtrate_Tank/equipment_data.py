"""
203-TA-401 BS FILTRATE TANK - modelling parameter set.

Source documents
----------------
* ``imports/900135359BS Filtrate Tank.pdf`` - ANDRITZ drawing 900135359 rev 0,
  "DDW FILTRATE TANK / MAIN DIMENSIONAL DRAWING", A1, 1:40, dated 07.07.2026,
  marked PRELIMINARY. Views: main elevation (1:30), A / B-B / C-C plans (1:50),
  D-D inspection hatch (1:20), E-E N9 overflow (1:15), F-F drain (1:10), two
  flat patterns (1:100 / 1:75), tank-anchoring detail.
* ``imports/900135359BS Filtrate Tank.pdf.dwg`` - the same drawing imported to
  AutoCAD 2025 with three added, proportionally scaled 1:1 view copies and
  nozzle-modification notes on layers PARAMETERS / AM_5 / FOUNDATION.

Every dimension below was measured numerically out of the DWG (converted to
DXF with LibreDWG), not scaled off the raster. The three added view copies are
drawn at 1:1 in model units, so a measured value IS a millimetre.

Datum and angular convention
----------------------------
Local frame, origin at the BOTTOM CENTRE of the tank (E 0 / N 0 / U 0), which
is the top of the flat bottom plate's underside - the foundation bearing plane.

Drawing azimuth is measured CLOCKWISE from the drawing's 0 mark, which is
modelled as North (user direction, 2026-09-21)::

    E = r * sin(az)        N = r * cos(az)
    E3D plan bearing (East -> North) = (90 - az) mod 360

The DWG also carries a "Plan View ... for Equipment Layout (Tank rotated 180
for installation based on site conditions)". That rotation is NOT baked in
here: the model is built in drawing orientation and the EQUI is rotated 180
about U when it is set out in the plant.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------

TAG = "203-TA-401"
ELEMENT = "203_TA_401"
NAME = "BS FILTRATE TANK (DDW FILTRATE TANK)"
DRAWING = "ANDRITZ 900135359 rev 0 (PRELIMINARY) + DWG nozzle modification"

# ---------------------------------------------------------------------------
# Shell / bottom / roof                                    [DWG, measured 1:1]
# ---------------------------------------------------------------------------

SHELL_ID = 6000.0          # "INSIDE 6000"
SHELL_T = 6.35             # measured 3006.35 - 3000.00
SHELL_OD = 6012.7
SHELL_TOP = 8000.0         # "8000 SHELL"
SHELL_PLATE_TOP = 8003.8   # top plate line, measured

BOTTOM_PLATE_OD = 6133.6   # measured R3066.8, 60 mm proud of the shell
BOTTOM_PLATE_T = 9.5

ROOF_SLOPE_DEG = 12.0      # annotated 12, measured 11.98
ROOF_EAVE_U = 8003.8       # roof plate at the shell
ROOF_COLLAR_OD = 1305.5    # measured R652.73 / R646.37
ROOF_CONE_TOP_U = 8504.7   # roof plate at the collar
ROOF_COLLAR_TOP_U = 8704.7 # deck plate line, measured
ROOF_DECK_T = 8.0          # REFERENCE VALUE

RAFTER_COUNT = 8           # measured at az 0/45/90/.../315
RAFTER_WIDTH = 80.0        # measured pair offset +-40
RAFTER_DEPTH = 163.0       # measured 8171.4 - 8008.4 at R2984.8
RAFTER_R_IN = 651.5
RAFTER_R_OUT = 2984.8

STIFFENER_ELEVATIONS = (3500.0, 5000.0, 6500.0)   # measured, L = 6211.4
STIFFENER_OD = 6212.0
STIFFENER_T = 9.5

OVERFLOW_LEVEL = 7375.0    # "7375 OVERFLOW LEVEL"

# ---------------------------------------------------------------------------
# Internals                                                [DWG, measured 1:1]
# ---------------------------------------------------------------------------

# Both air-separation cylinders share one axis, offset from the tank axis.
CYL_OFFSET_E = -501.9      # measured 33881.6 - 33379.7
CYL_OFFSET_N = 0.0

INNER_CYL_OD = 1515.2      # "1500" nominal; measured R757.61 / R751.25
INNER_CYL_ID = 1502.5
INNER_CYL_TOP = 5105.0     # "INNER CYLINDER 5105"

OUTER_CYL_OD = 2214.2      # "2200" nominal; measured R1107.12 / R1100.77
OUTER_CYL_ID = 2201.5
OUTER_CYL_TOP = 4298.0     # "OUTER CYLINDER 4298"

OUTER_CYL_BASE_RING_OD = 2372.7   # measured R1186.34
OUTER_CYL_BASE_RING_T = 12.0      # REFERENCE VALUE

# Four radial ribs between the two cylinders, measured about the cylinder axis.
RIB_AZIMUTHS = (35.5, 125.3, 213.8, 304.2)
RIB_T = 10.0                      # REFERENCE VALUE

SEP_WALL_T = 6.35          # = ROUT - RINS below; the same plate as the shell
SEP_WALL_TOP = 7800.0      # "7800 SEPARATION WALL"
# The wall is a TRUE CIRCULAR ARC. Both drawn faces fit a common centre to
# 0.002 mm over 33 points, measured off the MODIFIED C-C copy (so the 5 deg CCW
# rotation that goes with N1.2 is already in these numbers).
SEP_WALL_RINS = 9000.00    # fitted 8999.98
SEP_WALL_ROUT = 9006.35    # fitted 9006.33
# Arc centre in tank-local E/N, straight from the least-squares fit. Do NOT
# round these: the arc is 9 m in radius, so a 0.5 mm slip in the centre walks
# the far end several millimetres off the shell. The sector's start bearing and
# span are DERIVED in the builder from this centre so that both ends meet the
# shell bore by construction, rather than stored as rounded figures.
SEP_WALL_ARC_E = 10144.36
SEP_WALL_ARC_N = -2718.47
# For the record: centre at r 10502.29 / az 105.00 (110.00 as issued);
# ends on the shell bore at az 52.29 and 157.72; arc length 4830.3 at R9000.

LAUNDER_R_IN = 2400.0      # measured; "600" = 3000 - 2400
LAUNDER_R_OUT = 3000.0     # the shell bore is the outer wall
LAUNDER_AZ_START = 264.5   # measured radial end plates
LAUNDER_AZ_END = 339.6     # 75.1 deg span; chord at R2400 = 2921 (dimensioned)
LAUNDER_RIM_U = 5400.0     # "5400"
LAUNDER_FLOOR_U = 5170.0   # measured wall height 231
LAUNDER_PLATE_T = 8.0      # REFERENCE VALUE - not dimensioned
LAUNDER_DIVIDER_AZ = (276.4, 293.1, 309.8, 326.5)   # measured

# ---------------------------------------------------------------------------
# Nozzle schedule
# ---------------------------------------------------------------------------
# az_orig  = azimuth on the issued ANDRITZ drawing
# az       = azimuth after the DWG modification notes
# face_r   = radius of the flange face from the tank axis (mm)
# The PDF "LIST OF CONNECTIONS" sizes are superseded by the DWG notes where the
# two disagree; see the report's Reference Values section.

NOZZLES = (
    # mark     dn   elev    az_orig  az      face_r   service
    ("N1.1",  300, 4500.0,  336.8,  336.8,  3456.4, "Filtrate in - inner seal tank (2 x DN200 extraction filtrate combined)"),
    ("N1.2",  300, 4300.0,  155.4,  150.4,  3459.5, "Filtrate in - outer tank (2 x DN150 washing filtrate combined)"),
    ("N2.1",  250,  476.0,  180.0,    0.0,  3254.1, "Pump out - rotated 180 deg"),
    ("N2.2",  300,  476.0,   90.0,   60.0,  3301.9, "Pump out to digester displacement liquor tank - rotated 30 deg CCW"),
    ("N5",     80,  600.0,  165.0,  345.0,  3085.0, "Level instrument, PN40 pad flange - rotated 180 deg"),
    ("N6",    100,    0.0,   30.0,   15.0,  3301.2, "Drain - rotated 15 deg CCW"),
    ("N8",    300, 8809.4,    0.0,    0.0,     0.0, "Vent - roof centre, vertical"),
    ("N9",    300, 6589.0,   45.0,   30.0,  3544.2, "Overflow outlet - vertical down off the seal box"),
    ("N11",    15, 8000.0,   45.0,   30.0,  3222.6, "Overflow water in - seal box top"),
    ("N12",    25, 6389.0,   45.0,   30.0,  3222.6, "Overflow drain - seal box bottom"),
    ("N13",    80, 8283.0,   45.0,   30.0,  3544.2, "Overflow vent - seal box top"),
    ("MW",    600,  700.0,  270.0,  270.0,  3215.0, "Davit-type manway ID600"),
)

# N1.1 is a CHORD entry, not radial: it pierces the shell at az 336.8 and runs
# on a line whose outward bearing is 335.0, tangentially into the inner seal
# cylinder. Measured from the two pipe walls in the modified B-B copy
# (separation 325.7 = DN300 OD 323.9).
N1_1_PIERCE_AZ = 336.8
N1_1_AXIS_AZ = 335.0       # outward
N1_1_PROJECTION = 450.0    # REFERENCE VALUE - the drawn external run carries on
                           # past R3690 with no dimensioned face; standard
                           # projection for a DN300 shell nozzle with a pad.

# Overflow-assembly nozzle lengths. The three with a dimension on E-E use it.
N9_LENGTH = 300.0          # REFERENCE VALUE - stub below the seal box
N11_LENGTH = 50.0          # E-E "50"
N12_LENGTH = 200.0         # E-E "200"
N13_LENGTH = 333.0         # E-E "333"

# N5 pad flange, measured: pad from the shell face out to R3051.8, ~200 wide.
N5_PAD_R_OUT = 3051.8
N5_PAD_W = 200.0

# ---------------------------------------------------------------------------
# Non-piping shell furniture
# ---------------------------------------------------------------------------

IH_R = 1934.4              # inspection hatch centre radius, measured
IH_AZ = 349.6
IH_OPENING_D = 500.0       # "500" in the connection list
IH_CURB_OD = 670.0         # measured R335.1
IH_CURB_U = 8180.0         # measured curb 8189..8284
IH_CURB_H = 120.0
IH_COVER_OD = 720.0        # REFERENCE VALUE - overhang not dimensioned
IH_COVER_T = 15.0          # REFERENCE VALUE
IH_COVER_U = 8300.0        # measured second feature 8301..8400

NP_AZ = 290.0              # nameplate, measured 287.9..292.1
NP_U = 1200.0              # "1200 NP"
NP_R = 3144.0
NP_W = 220.0
NP_T = 8.0                 # REFERENCE VALUE - not dimensioned
NP_H = 150.0               # REFERENCE VALUE - not dimensioned

GL_AZIMUTHS = (10.0, 100.0, 190.0, 280.0)   # 4 off, measured in views A and C-C
GL_U = 300.0               # REFERENCE VALUE - elevation not dimensioned
GL_PROJECTION = 150.0      # measured r 3156 vs shell OD 3006.35
GL_W = 60.0                # REFERENCE VALUE
GL_T = 12.0                # REFERENCE VALUE

ANCHOR_AZIMUTHS = (15.0, 75.0, 135.0, 195.0, 255.0, 315.0)   # 6 off, measured
ANCHOR_PAD_U = 700.0
ANCHOR_PAD_H = 300.0
ANCHOR_PAD_W = 250.0
ANCHOR_PROJECTION = 150.0
ANCHOR_STRAP_W = 150.0     # "150" on the TANK ANCHORING detail
ANCHOR_STRAP_T = 20.0
ANCHOR_PLATE = 200.0       # DWG: "Embedded steel plate, 200x200x10 mm"
ANCHOR_PLATE_T = 10.0

# ---------------------------------------------------------------------------
# N9 overflow seal box (E-E 1:15)
# ---------------------------------------------------------------------------

OVF_AZ = 30.0
OVF_BOTTOM_U = 6589.0      # "6589 N9"
OVF_TOP_U = 7950.0         # 6589 + 1361 (E-E total height)
OVF_HEIGHT = 1361.0
OVF_BOX_RADIAL = 400.0     # E-E "350" internal + 5 mm plate each side
OVF_BOX_TANGENTIAL = 500.0 # REFERENCE VALUE - E-E is a section; only the 350
                           # radial dimension is given
OVF_PLATE_T = 5.0          # E-E "5" on the box and the downcomer wall
OVF_PIPE_OD = 323.9        # E-E "323,9"
OVF_PIPE_R = 3544.2        # view A "3542", measured 3544.2
OVF_OPENING_H = 250.0      # E-E "OPENING TO SHELL 250"
OVF_OPENING_BASE_U = 6975.0  # 6589 + 386

# ---------------------------------------------------------------------------
# Process / design data (drawing TECHNICAL DATA block) - carried for the report
# ---------------------------------------------------------------------------

DESIGN = {
    "design_code": "EN14015 / API650",
    "design_pressure_kpag": "2 + hydr. (max) / -2 (min)",
    "design_temperature_c": "100 (max) / 0 (min)",
    "nominal_volume_m3": 226.0,
    "medium_density_kgm3": 1050.0,
    "contents": "Filtrate",
    "material": "1.4307 or equal",
    "roof_load": "2 kN/m2 distributed",
    "insulation": "HOLD - for personnel protection",
}
