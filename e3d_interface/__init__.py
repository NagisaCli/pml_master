"""
E3D Interaction Interface
=========================
Provides interaction with AVEVA E3D Design environment:
  1. PML script execution (command-line mode)
  2. .NET API bridging (COM/.NET assembly calls)
  3. File generation for manual loading

Note: Actual E3D interaction requires E3D Design installed.
"""

import subprocess
import os
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime

from ..config import E3D_DESIGN_EXE, PROJECT_ROOT, ensure_output_dir
from ..memory import MemoryStore


class E3DInterface:
    """
    E3D interaction interface for paper mill modeling.

    Three execution modes:
      1. FILE — Generate PML file for manual execution in E3D
      2. CMD  — Invoke E3D Design from command line
      3. API  — Interact via .NET Add-in API (requires Add-in deployment)
    """

    def __init__(self, memory_store: Optional[MemoryStore] = None):
        self.memory = memory_store or MemoryStore()
        self._check_environment()

    def _check_environment(self):
        """Check whether the E3D runtime environment is available."""
        self.e3d_available = Path(E3D_DESIGN_EXE).exists()
        self.env_ready = False
        if self.e3d_available:
            self.env_ready = "AVEVA_DESIGN_EXE" in os.environ
            if not self.env_ready:
                print(f"[E3D] des.exe found, but environment variables are not set")
                print(f"[E3D] Please run: call \"D:\\AVEVA\\Everything3D3.1\\evars\" "
                      f"\"D:\\AVEVA\\Everything3D3.1\"")
                print(f"[E3D] Falling back to file mode — generating .pml for manual loading\n")
        else:
            print(f"[E3D] E3D Design not detected ({E3D_DESIGN_EXE})")
            print(f"[E3D] Using file mode — generating .pml file for manual execution\n")

    # -- Mode 1: File Mode --------------------------------------------

    def execute_file_mode(self, pml_script: str, script_name: str = "") -> str:
        """Save PML script to file and return path for manual execution."""
        if not script_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            script_name = f"e3d_agent_{timestamp}.pml"

        filepath = ensure_output_dir() / script_name
        with open(filepath, "w", encoding="utf-8", newline="\n") as f:
            f.write(pml_script)

        print(f"[E3D] PML script saved: {filepath}")
        print(f"[E3D] To execute in E3D Design:")
        print(f"      1. Open E3D Design")
        print(f"      2. Select writable ZONE")
        print(f"      3. Enter: $$MACRO {filepath}")
        return str(filepath)

    # -- Mode 2: Command-Line Mode ------------------------------------

    def execute_cmd_mode(self, pml_script: str, timeout: int = 300) -> Dict:
        """
        Execute PML script via E3D Design command line.
        Requires E3D Design installed and evars environment configured.
        """
        if not self.e3d_available:
            return self._fallback_to_file(pml_script, "E3D Design not available")
        if not self.env_ready:
            return self._fallback_to_file(
                pml_script,
                "E3D environment variables not configured (run evars.bat first)"
            )

        # Save temporary script
        tmp_file = ensure_output_dir() / f"_tmp_exec_{datetime.now().strftime('%H%M%S_%f')}.pml"
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
                error_msg = f"E3D returned error code {result.returncode}: {result.stderr}"
                self._log_error("EXEC_CMD", error_msg, {
                    "script": pml_script[:500],
                    "returncode": result.returncode,
                })
                return {"success": False, "output": output, "error": error_msg}

        except FileNotFoundError:
            msg = f"E3D Design executable not found: {E3D_DESIGN_EXE}"
            self._log_error("EXEC_CMD", msg, {"script_path": str(tmp_file)})
            return self._fallback_to_file(pml_script, msg)
        except subprocess.TimeoutExpired:
            msg = f"PML script execution timed out ({timeout}s)"
            self._log_error("EXEC_TIMEOUT", msg, {"script_path": str(tmp_file)})
            return {"success": False, "output": "", "error": msg}
        except Exception as e:
            msg = f"E3D execution exception: {e}"
            self._log_error("EXEC_EXCEPTION", msg, {"script_path": str(tmp_file)})
            return {"success": False, "output": "", "error": msg}
        finally:
            if tmp_file.exists():
                tmp_file.unlink()

    # -- Mode 3: .NET API Bridge --------------------------------------

    def execute_dotnet_api(self, csharp_code: str) -> Dict:
        """
        Create E3D elements via .NET Add-in API.
        Requires the E3DAddinBridge add-in to be pre-deployed.
        """
        if not self.e3d_available:
            return self._fallback_to_file(
                csharp_code,
                ".NET API requires E3D runtime; generating PML wrapper code instead"
            )

        dotnet_api_available = (
            Path(E3D_DESIGN_EXE).exists() and
            (Path(E3D_DESIGN_EXE).parent / "Aveva.Core.Database.dll").exists()
        )
        if not dotnet_api_available:
            msg = ".NET API assembly not found (requires des.exe + Aveva.Core.Database.dll)"
            self._log_error("DOTNET_ASSEMBLY", msg, {})
            return {"success": False, "output": "", "error": msg}

        return {
            "success": False,
            "output": "",
            "error": (
                "The .NET API path is not implemented. It previously emitted a "
                "PML wrapper built from !!DotNetLoad, !result = and IF/THEN/ENDIF "
                "- all PML2 constructs banned by Iron Rule 3, so the generated "
                "macro could never load in E3D. Passing C# source as a PML string "
                "argument would not have compiled either. Use execute_file_mode "
                "or execute_cmd_mode, which emit PML1 and are verified."
            ),
        }

    # -- Project Status Queries ---------------------------------------

    def get_project_info(self) -> Dict:
        """Get current E3D project information."""
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

    # -- Internal Methods ---------------------------------------------

    def _fallback_to_file(self, content: str, reason: str) -> Dict:
        """Fallback when E3D is unavailable: save as file."""
        filepath = self.execute_file_mode(
            content, f"fallback_{datetime.now().strftime('%H%M%S')}.pml"
        )
        return {
            "success": True,
            "output": f"Falling back to file mode (reason: {reason})",
            "error": "",
            "file": filepath,
        }

    def _log_error(self, module: str, error_text: str, context: Dict):
        """Log an error to the memory system."""
        if self.memory:
            self.memory.add_error(
                module=f"E3DInterface.{module}",
                error_text=error_text,
                context=context,
            )
