"""
Fly Language CLI
Entry point for the `fly` command
"""

import sys
import os
import argparse
from pathlib import Path


BANNER = r"""
  ███████╗██╗  ██╗   ██╗
  ██╔════╝██║  ╚██╗ ██╔╝
  █████╗  ██║   ╚████╔╝ 
  ██╔══╝  ██║    ╚██╔╝  
  ██║     ███████╗██║   
  ╚═╝     ╚══════╝╚═╝   
  Fly Language v1.0.0
  Professional Scripting + Kali Integration
"""


def main():
    if len(sys.argv) < 2:
        print(BANNER)
        print("Usage: fly <command> [options]")
        print()
        print("Commands:")
        print("  fly run <file.fy>          Run a .fy script")
        print("  fly <file.fy>              Same as run")
        print("  fly repl                   Launch interactive REPL")
        print("  fly install <tool>         Install a Kali tool")
        print("  fly remove <tool>          Remove a tool")
        print("  fly list                   List installed tools")
        print("  fly search <query>         Search available tools")
        print("  fly update                 Update installed tools")
        print("  fly transpile <file.fy>    Show transpiled Python code")
        print("  fly new <script.fy>        Create a new .fy script template")
        print("  fly version                Show version info")
        print()
        print("Examples:")
        print("  fly osint.fy")
        print("  fly install wafw00f")
        print("  fly install nmap")
        print("  fly run scanner.fy --target 192.168.1.1")
        sys.exit(0)

    command = sys.argv[1]

    # Direct file execution: fly script.fy
    if command.endswith(".fy") or command.endswith(".fly"):
        _cmd_run(command, sys.argv[2:])
        return

    if command in ("run", "r"):
        if len(sys.argv) < 3:
            print("[fly] Error: Specify a .fy file to run.")
            print("  fly run script.fy")
            sys.exit(1)
        _cmd_run(sys.argv[2], sys.argv[3:])

    elif command == "repl":
        _cmd_repl()

    elif command == "install":
        if len(sys.argv) < 3:
            print("[fly] Error: Specify a tool name.")
            print("  fly install wafw00f")
            sys.exit(1)
        method = "auto"
        if "--apt" in sys.argv:
            method = "apt"
        elif "--pip" in sys.argv:
            method = "pip"
        from .tools.manager import install_tool
        install_tool(sys.argv[2], method=method)

    elif command in ("remove", "uninstall"):
        if len(sys.argv) < 3:
            print("[fly] Error: Specify a tool name.")
            sys.exit(1)
        from .tools.manager import remove_tool
        remove_tool(sys.argv[2])

    elif command in ("list", "ls"):
        from .tools.manager import list_tools
        list_tools()

    elif command == "search":
        if len(sys.argv) < 3:
            print("[fly] Error: Specify a search query.")
            sys.exit(1)
        from .tools.manager import search_tools
        search_tools(sys.argv[2])

    elif command == "update":
        from .tools.manager import update_tools
        update_tools()

    elif command == "transpile":
        if len(sys.argv) < 3:
            print("[fly] Error: Specify a .fy file.")
            sys.exit(1)
        from .interpreter import show_transpiled
        show_transpiled(sys.argv[2])

    elif command == "new":
        if len(sys.argv) < 3:
            print("[fly] Error: Specify a filename.")
            print("  fly new myscript.fy")
            sys.exit(1)
        _cmd_new(sys.argv[2])

    elif command == "version":
        _cmd_version()

    elif command == "help":
        main.__doc__ and print(main.__doc__)
        os.execv(sys.executable, [sys.executable, "-m", "fly"] + [])

    else:
        # Try to run as a tool
        from .tools.manager import run_tool
        exit_code = run_tool(command, sys.argv[2:])
        sys.exit(exit_code or 0)


def _cmd_run(filepath: str, extra_args: list):
    from .interpreter import run_file
    run_file(filepath, args=extra_args)


def _cmd_repl():
    from .interpreter import interactive_shell
    interactive_shell()


def _cmd_version():
    from . import __version__
    print(f"Fly Language v{__version__}")
    print("Python backend:", sys.version)
    print("Platform:", sys.platform)


def _cmd_new(filename: str):
    if not filename.endswith((".fy", ".fly")):
        filename = filename + ".fy"

    path = Path(filename)
    if path.exists():
        print(f"[fly] Error: {filename} already exists.")
        sys.exit(1)

    template = f'''## {filename} - Fly Script
## Created with Fly Language v1.0.0

use os
use sys

fn main():
    say "Hello from Fly!"
    say f"Running on: {{sys.platform}}"

    ## Example: shell command
    # shell("whoami")

    ## Example: quick scan
    # scan("192.168.1.1", ports="80,443")

    ## Example: recon
    # recon("example.com")

main()
'''
    path.write_text(template, encoding="utf-8")
    print(f"[fly] ✓ Created {filename}")
    print(f"[fly] Run it with: fly {filename}")
