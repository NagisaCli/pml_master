"""
E3D 交互接口
===========
提供与 AVEVA E3D 设计环境的交互能力：
  1. PML 脚本执行（命令行模式）
  2. .NET API 桥接（COM/.NET 程序集调用）
  3. 项目状态查询

注意：
  实际 E3D 交互需要运行环境（E3D Design 安装）。
  当前模块提供接口框架 + PML 文件生成能力。
  E3D 实际执行需要用户手动操作。
"""

import subprocess
import os
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime

from ..config import E3D_DESIGN_EXE, PROJECT_ROOT, PML_OUTPUT_DIR
from ..memory import MemoryStore


class E3DInterface:
    """
    E3D 交互接口。

    三种执行模式：
      1. FILE — 生成 PML 文件，用户手动在 E3D 中运行
      2. CMD  — 通过命令行调用 E3D Design 执行 PML
      3. API  — 通过 .NET Add-in API 交互（需部署 Add-in）
    """

    def __init__(self, memory_store: Optional[MemoryStore] = None):
        self.memory = memory_store or MemoryStore()
        self._check_environment()

    def _check_environment(self):
        """检查 E3D 运行环境是否可用。"""
        self.e3d_available = Path(E3D_DESIGN_EXE).exists()
        self.env_ready = False
        if self.e3d_available:
            # 检查是否从 evars/launch.bat 设置过环境变量
            self.env_ready = "AVEVA_DESIGN_EXE" in os.environ
            if not self.env_ready:
                print(f"[E3D] des.exe 已找到，但环境变量未设置")
                print(f"[E3D] 请先执行以下命令初始化环境:")
                print(f'      call "D:\\AVEVA\\Everything3D3.1\\evars" "D:\\AVEVA\\Everything3D3.1"')
                print(f"[E3D] 或通过 launch.bat 启动 E3D")
                print(f"[E3D] 当前自动降级到文件模式 — 生成 .pml 供手动加载\n")
        else:
            print(f"[E3D] E3D Design 未检测到 ({E3D_DESIGN_EXE})")
            print(f"[E3D] 当前使用文件模式 — 生成 .pml 文件供用户手动执行\n")

    # ── 模式 1: 文件模式 ─────────────────────

    def execute_file_mode(self, pml_script: str, script_name: str = "") -> str:
        """
        保存 PML 脚本到文件，返回文件路径供用户手动执行。
        """
        from ..config import PML_OUTPUT_DIR
        if not script_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            script_name = f"e3d_agent_{timestamp}.pml"

        filepath = PML_OUTPUT_DIR / script_name
        with open(filepath, "w", encoding="utf-8", newline="\n") as f:
            f.write(pml_script)

        print(f"[E3D] PML 脚本已保存: {filepath}")
        print(f"[E3D] 请在 E3D Design 中执行:")
        print(f"      1. 打开 E3D Design")
        print(f"      2. 在命令栏输入: $$MACRO {filepath}")
        return str(filepath)

    # ── 模式 2: 命令行模式 ───────────────────

    def execute_cmd_mode(self, pml_script: str, timeout: int = 300) -> Dict:
        """
        通过 E3D Design 命令行执行 PML 脚本。
        需要 E3D Design 安装且通过 evars 配置好环境变量。

        Args:
            pml_script: PML 脚本内容
            timeout: 超时（秒）

        Returns:
            {"success": bool, "output": str, "error": str}
        """
        if not self.e3d_available:
            return self._fallback_to_file(pml_script, "E3D Design 不可用")
        if not self.env_ready:
            return self._fallback_to_file(
                pml_script,
                "E3D 环境变量未配置 (需要先执行 evars.bat)"
            )

        # 保存临时脚本
        tmp_file = PML_OUTPUT_DIR / f"_tmp_exec_{datetime.now().strftime('%H%M%S_%f')}.pml"
        with open(tmp_file, "w", encoding="utf-8", newline="\n") as f:
            f.write(pml_script)

        try:
            result = subprocess.run(
                [E3D_DESIGN_EXE, "/MACRO", str(tmp_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(PROJECT_ROOT),
            )
            output = result.stdout + "\n" + result.stderr
            if result.returncode == 0:
                return {"success": True, "output": output, "error": ""}
            else:
                error_msg = f"E3D 返回错误码 {result.returncode}: {result.stderr}"
                self._log_error("EXEC_CMD", error_msg, {
                    "script": pml_script[:500],
                    "returncode": result.returncode,
                })
                return {"success": False, "output": output, "error": error_msg}

        except FileNotFoundError:
            msg = f"E3D Design 可执行文件未找到: {E3D_DESIGN_EXE}"
            self._log_error("EXEC_CMD", msg, {"script_path": str(tmp_file)})
            return self._fallback_to_file(pml_script, msg)
        except subprocess.TimeoutExpired:
            msg = f"PML 脚本执行超时 ({timeout}s)"
            self._log_error("EXEC_TIMEOUT", msg, {"script_path": str(tmp_file)})
            return {"success": False, "output": "", "error": msg}
        except Exception as e:
            msg = f"E3D 执行异常: {e}"
            self._log_error("EXEC_EXCEPTION", msg, {"script_path": str(tmp_file)})
            return {"success": False, "output": "", "error": msg}
        finally:
            if tmp_file.exists():
                tmp_file.unlink()

    # ── 模式 3: .NET API 桥接 ────────────────

    def execute_dotnet_api(self, csharp_code: str) -> Dict:
        """
        通过 .NET Add-in API 创建 E3D 元素。
        需要预先部署 E3DAddinBridge 插件。
        当前返回 API 调用所需的 PML 包装代码。
        """
        if not self.e3d_available:
            return self._fallback_to_file(
                csharp_code,
                ".NET API 需要 E3D 运行时，生成 PML 包装代码替代"
            )

        # 检查 AVEVA .NET API 程序集是否存在
        dotnet_api_available = (
            Path(E3D_DESIGN_EXE).exists() and
            (Path(E3D_DESIGN_EXE).parent / "Aveva.Core.Database.dll").exists()
        )
        if not dotnet_api_available:
            msg = f".NET API 程序集未找到 (需要 des.exe + Aveva.Core.Database.dll)"
            self._log_error("DOTNET_ASSEMBLY", msg, {})
            return {"success": False, "output": "", "error": msg}

        # 生成 PML 调用 .NET 的包装代码
        pml_wrapper = self._wrap_csharp_as_pml(csharp_code)
        return self.execute_cmd_mode(pml_wrapper)

    def _wrap_csharp_as_pml(self, csharp_code: str) -> str:
        """
        将 C# 代码包装为 PML 可调用的形式。
        实际使用中需要预装 Add-in，PML 通过 DotNetCall 调用。
        """
        lines = [
            "-- ========================================",
            "-- .NET API 调用包装 — PML 桥接",
            "-- 需要在 E3D 中预装 AVEVA.AddinBridge",
            "-- ========================================",
            "",
            "-- 加载桥接程序集",
            "!!DotNetLoad('AVEVA.AddinBridge.dll')",
            "",
            "-- 调用 .NET 创建方法",
            "!result = !!DotNetCall(",
            "    'AVEVA.AddinBridge.E3DModelBuilder'",
            "    , 'CreateElements'",
            f"    , `{csharp_code}`",
            ")",
            "",
            "IF !result THEN",
            "   -- 元素创建成功",
            "ELSE",
            "   -- 创建失败，请检查 C# 代码和 E3D 环境",
            "ENDIF",
        ]
        return "\n".join(lines)

    # ── 项目状态查询 ─────────────────────────

    def get_project_info(self) -> Dict:
        """获取当前 E3D 项目信息。"""
        info = {
            "project_root": str(PROJECT_ROOT),
            "e3d_available": self.e3d_available,
            "sub_projects": [],
        }
        from ..config import SUB_PROJECTS
        for code, sp in SUB_PROJECTS.items():
            db_dir = sp["database"]
            db_files = list(db_dir.glob("*_0001")) if db_dir.exists() else []
            info["sub_projects"].append({
                "code": code,
                "name": sp["path"].name,
                "type": sp["type"],
                "db_path": str(db_dir),
                "db_files_count": len(db_files),
                "exists": db_dir.exists(),
            })
        return info

    # ── 内部方法 ──────────────────────────────

    def _fallback_to_file(self, content: str, reason: str) -> Dict:
        """E3D 不可用时的降级：保存为文件。"""
        filepath = self.execute_file_mode(content, f"fallback_{datetime.now().strftime('%H%M%S')}.pml")
        return {
            "success": True,
            "output": f"降级到文件模式 (原因: {reason})",
            "error": "",
            "file": filepath,
        }

    def _log_error(self, module: str, error_text: str, context: Dict):
        """记录错误到记忆系统。"""
        if self.memory:
            self.memory.add_error(
                module=f"E3DInterface.{module}",
                error_text=error_text,
                context=context,
            )
