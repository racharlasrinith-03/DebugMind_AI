
import ast
import subprocess
import sys
from pathlib import Path


def run_code(file_path="generated_code.py", timeout=60):
    file_path = Path(file_path)

    if not file_path.exists():
        return False, "ERROR: Generated Python file does not exist."

    try:
        code = file_path.read_text(encoding="utf-8")
        # Check syntax without executing the program.
        ast.parse(code, filename=str(file_path))

    except SyntaxError as e:
        return False, (
            f"SYNTAX ERROR: {e.msg}\n"
            f"Line: {e.lineno}\n"
            f"Code: {e.text}"
        )

    except OSError as e:
        return False, f"FILE ERROR: {e}"

    try:
        result = subprocess.run(
            [sys.executable, "-u", str(file_path.resolve())],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(file_path.resolve().parent)
        )

        output = result.stdout.strip()
        errors = result.stderr.strip()

        if result.returncode == 0:
            return True, output or "Program executed successfully with no output."

        return False, (
            f"RUNTIME ERROR (exit code {result.returncode})\n"
            f"STDOUT:\n{output or '(empty)'}\n"
            f"STDERR:\n{errors or '(empty)'}"
        )

    except subprocess.TimeoutExpired:
        return False, (
            f"TIMEOUT: Program exceeded {timeout} seconds. "
            "Check for infinite loops, blocking input, or expensive computation. "
            "If the task legitimately needs more time, increase the timeout."
        )

    except OSError as e:
        return False, f"EXECUTION ERROR: {e}"
