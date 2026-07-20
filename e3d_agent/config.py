"""
E3D Agent 配置
==============
项目特定的配置，从现有项目文件自动检测或手动设置。
"""

from pathlib import Path
import os

# ─── 项目路径 ─────────────────────────────────
PROJECT_ROOT = Path(os.environ.get(
    "E3D_PROJECT_ROOT",
    r"D:\AVEVA\Projects\E3D3.1"
))

# ─── 子项目映射 ───────────────────────────────
# 从 custom_evars.bat / evars*.bat 推断
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

# ─── PML 执行配置 ─────────────────────────────
# E3D DESIGN 命令行路径（根据实际安装路径修改）
E3D_DESIGN_EXE = os.environ.get(
    "E3D_DESIGN_EXE",
    r"D:\AVEVA\Everything3D3.1\des.exe"
)

# .NET 管理程序集路径
E3D_ADMIN_DIR = os.environ.get(
    "E3D_ADMIN_DIR",
    r"D:\AVEVA\Everything3D3.1"
)

# PML 宏输出目录
PML_OUTPUT_DIR = PROJECT_ROOT / "e3d_agent" / "output"
PML_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── 图纸目录 ─────────────────────────────────
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

# ─── 记忆系统配置 ─────────────────────────────
MEMORY_DB_PATH = PROJECT_ROOT / "e3d_agent" / "memory" / "memory_store.json"
MAX_MEMORY_ENTRIES = 500

# ─── LLM 配置 ─────────────────────────────────
# 使用系统级 LLM（Hermes 的 LLM），不单独配置 API Key
LLM_USE_SYSTEM = True
