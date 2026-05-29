"""
Fly Language Interpreter
Runs .fy files by transpiling them to Python and executing
"""

import sys
import os
import traceback
import tempfile
from pathlib import Path
from .lexer import transpile


def run_file(filepath: str, args: list = None):
    """
    Run a .fy file.
    
    Args:
        filepath: Path to the .fy file
        args: Additional arguments passed to the script
    """
    path = Path(filepath)

    if not path.exists():
        print(f"[fly] Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    if path.suffix not in (".fy", ".fly"):
        print(f"[fly] Warning: Expected .fy extension, got {path.suffix}", file=sys.stderr)

    source = path.read_text(encoding="utf-8")

    # Pass script args
    if args:
        sys.argv = [filepath] + args
    else:
        sys.argv = [filepath]

    # Add file's directory to sys.path
    sys.path.insert(0, str(path.parent.resolve()))

    python_code = transpile(source)

    # Execute in a clean namespace
    namespace = {
        "__name__": "__main__",
        "__file__": str(path.resolve()),
        "__fly_version__": "1.0.0",
    }

    try:
        exec(compile(python_code, filepath, "exec"), namespace)
    except SystemExit:
        raise
    except Exception:
        # Show error with .fy file reference
        tb = traceback.format_exc()
        tb = tb.replace('<string>', filepath)
        print(f"\n[fly] Runtime error in {filepath}:", file=sys.stderr)
        print(tb, file=sys.stderr)
        sys.exit(1)


def run_string(source: str, filename: str = "<fly>"):
    """Run Fly source code from a string."""
    python_code = transpile(source)
    namespace = {
        "__name__": "__main__",
        "__file__": filename,
        "__fly_version__": "1.0.0",
    }
    exec(compile(python_code, filename, "exec"), namespace)


def show_transpiled(filepath: str):
    """Show the transpiled Python code without executing."""
    path = Path(filepath)
    if not path.exists():
        print(f"[fly] Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    source = path.read_text(encoding="utf-8")
    python_code = transpile(source)
    print(python_code)


def interactive_shell():
    """Launch the Fly interactive REPL."""
    import code
    from .lexer import transpile

    print("Fly Language REPL v1.0.0")
    print("Type 'exit()' or Ctrl+D to quit")
    print("=" * 40)

    namespace = {
        "__name__": "__console__",
        "__fly_version__": "1.0.0",
    }

    # Bootstrap builtins
    from .lexer import _build_header
    exec(_build_header(), namespace)

    while True:
        try:
            line = input("fly> ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not line.strip():
            continue

        from .lexer import transpile_line
        try:
            py_line = transpile_line(line)
            exec(compile(py_line, "<fly-repl>", "single"), namespace)
        except SystemExit:
            break
        except Exception as e:
            print(f"[fly] Error: {e}")
