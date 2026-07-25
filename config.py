"""
E3D Agent Configuration
=======================
Paths and modeling defaults, resolved from environment variables so the package
works on any machine without editing source.

Environment variables
---------------------
``E3D_PROJECT_ROOT``
    AVEVA project root. Defaults to ``D:/AVEVA/Projects/E3D3.1``, the usual
    Windows install location.
``E3D_DESIGN_EXE``
    Path to ``des.exe``. Only needed to execute macros directly; generation
    works without E3D installed.
``E3D_ADMIN_DIR``
    Directory holding the E3D .NET admin assemblies.
``E3D_OUTPUT_DIR``
    Where generated ``.pml`` macros are written. Defaults to ``output/`` beside
    this file, so a missing or read-only project drive does not break generation.
"""

from pathlib import Path
import os

# --- Package location -----------------------------------------------------

PACKAGE_ROOT = Path(__file__).resolve().parent

# --- Project paths --------------------------------------------------------

PROJECT_ROOT = Path(os.environ.get(
    "E3D_PROJECT_ROOT",
    r"D:\AVEVA\Projects\E3D3.1"
))

# --- Sub-project mapping --------------------------------------------------
# Derived from the project evars batch files.
SUB_PROJECTS = {
    "ACP": {
        "prefix": "acp",
        "code": "ACP",
        "path": PROJECT_ROOT / "AvevaCatalogue",
        "database": PROJECT_ROOT / "AvevaCatalogue" / "acp000",
        "type": "catalogue",
    },
    "APS": {
        "prefix": "aps",
        "code": "APS",
        "path": PROJECT_ROOT / "AvevaPlantSample",
        "database": PROJECT_ROOT / "AvevaPlantSample" / "aps000",
        "type": "plant",
    },
    "AMS": {
        "prefix": "ams",
        "code": "AMS",
        "path": PROJECT_ROOT / "AvevaMarineSample",
        "database": PROJECT_ROOT / "AvevaMarineSample" / "ams000",
        "type": "marine",
    },
}

# --- PML execution configuration ------------------------------------------

E3D_DESIGN_EXE = os.environ.get(
    "E3D_DESIGN_EXE",
    r"D:\AVEVA\Everything3D3.1\des.exe"
)

E3D_ADMIN_DIR = os.environ.get(
    "E3D_ADMIN_DIR",
    r"D:\AVEVA\Everything3D3.1"
)

# Output lives beside the package by default. The previous location was under
# PROJECT_ROOT, which made importing this module fail on any machine without the
# AVEVA project drive mounted, since the directory was created at import time.
PML_OUTPUT_DIR = Path(os.environ.get("E3D_OUTPUT_DIR", PACKAGE_ROOT / "output"))


def ensure_output_dir() -> Path:
    """
    Create and return the macro output directory.

    Called when a macro is about to be written rather than at import, so merely
    importing the package never touches the filesystem.
    """
    PML_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return PML_OUTPUT_DIR


# --- Project data ---------------------------------------------------------

#: JK-Project source data: equipment list and reference drawings.
JK_PROJECT_DIR = PACKAGE_ROOT / "JK-Project"
EQUIPMENT_LIST_XLSX = JK_PROJECT_DIR / "Modeling_lists.xlsx"
TOP_VIEW_DIR = JK_PROJECT_DIR / "Model_Reference(All_Top_View)"
SIDE_VIEW_DIR = JK_PROJECT_DIR / "Model_reference(Part_Side_View)"

# --- Drawing directories --------------------------------------------------

DRAWING_DIRS = {
    "svg": PROJECT_ROOT / "AvevaMarineSample" / "amsdia",
    "dwg": {
        "ACP": PROJECT_ROOT / "AvevaCatalogue" / "acpdwg",
        "APS": PROJECT_ROOT / "AvevaPlantSample" / "apsdwg",
        "AMS": PROJECT_ROOT / "AvevaMarineSample" / "amsdwg",
    },
    "pic": {
        "ACP": PROJECT_ROOT / "AvevaCatalogue" / "acppic",
        "APS": PROJECT_ROOT / "AvevaPlantSample" / "apspic",
        "AMS": PROJECT_ROOT / "AvevaMarineSample" / "amspic",
    },
}

# --- Memory system --------------------------------------------------------

MEMORY_DB_PATH = Path(
    os.environ.get("E3D_MEMORY_PATH", PACKAGE_ROOT / "memory" / "memory_store.json")
)
MAX_MEMORY_ENTRIES = 500

# --- LLM configuration ----------------------------------------------------

LLM_USE_SYSTEM = True

# --- Paper machine reference dimensions (mm) ------------------------------

PAPER_MACHINE_DEFAULTS = {
    "trim_width": 4800,
    "wire_width": 5200,
    "dryer_diameter": 1800,
    "dryer_pitch": 2400,
    "dryer_face": 5400,
    "dryer_count": 40,
    "press_nips": 3,
    "machine_speed_m_min": 500,
    "breast_roll_diameter": 800,
    "couch_roll_diameter": 1000,
    "calender_roll_diameter": 800,
    "reel_drum_diameter": 1100,
}
