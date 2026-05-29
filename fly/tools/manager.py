"""
Fly Tool Manager
Handles fly install / fly remove / fly list / fly run
"""

import subprocess
import sys
import os
import json
import shutil
from pathlib import Path

TOOLS_DB_PATH = Path.home() / ".fly" / "tools.json"
TOOLS_DIR = Path.home() / ".fly" / "tools"


def _ensure_dirs():
    TOOLS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)


def _load_db() -> dict:
    _ensure_dirs()
    if TOOLS_DB_PATH.exists():
        return json.loads(TOOLS_DB_PATH.read_text())
    return {}


def _save_db(db: dict):
    _ensure_dirs()
    TOOLS_DB_PATH.write_text(json.dumps(db, indent=2))


def install_tool(name: str, method: str = "auto"):
    """
    Install a tool.
    Tries apt-get, then pip, then git clone.
    """
    db = _load_db()

    if name in db:
        print(f"[fly] '{name}' is already installed.")
        return

    print(f"[fly] Installing {name}...")

    # Try apt-get first (Kali/Debian tools)
    if method in ("auto", "apt"):
        ret = subprocess.run(
            ["sudo", "apt-get", "install", "-y", name],
            capture_output=True, text=True
        )
        if ret.returncode == 0:
            db[name] = {"method": "apt", "version": "latest"}
            _save_db(db)
            print(f"[fly] ✓ {name} installed via apt.")
            return
        elif method == "apt":
            print(f"[fly] ✗ apt install failed for {name}")
            print(ret.stderr)
            return

    # Try pip
    if method in ("auto", "pip"):
        ret = subprocess.run(
            [sys.executable, "-m", "pip", "install", name],
            capture_output=True, text=True
        )
        if ret.returncode == 0:
            db[name] = {"method": "pip", "version": "latest"}
            _save_db(db)
            print(f"[fly] ✓ {name} installed via pip.")
            return
        elif method == "pip":
            print(f"[fly] ✗ pip install failed for {name}")
            print(ret.stderr)
            return

    print(f"[fly] ✗ Could not install {name}. Try: sudo apt install {name}")


def remove_tool(name: str):
    """Remove an installed tool."""
    db = _load_db()

    if name not in db:
        print(f"[fly] '{name}' is not in the fly tools registry.")
        return

    method = db[name].get("method", "apt")

    if method == "apt":
        subprocess.run(["sudo", "apt-get", "remove", "-y", name])
    elif method == "pip":
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", name])

    del db[name]
    _save_db(db)
    print(f"[fly] ✓ {name} removed.")


def list_tools():
    """List all installed tools."""
    db = _load_db()

    if not db:
        print("[fly] No tools installed. Use: fly install <toolname>")
        return

    print("[fly] Installed tools:")
    print("-" * 40)
    for name, info in sorted(db.items()):
        method = info.get("method", "?")
        print(f"  {name:<25} [{method}]")
    print("-" * 40)
    print(f"  Total: {len(db)} tools")


def run_tool(name: str, args: list = None):
    """Run an installed tool with arguments."""
    args = args or []

    if not shutil.which(name):
        print(f"[fly] '{name}' not found in PATH.")
        print(f"[fly] Try: fly install {name}")
        return 1

    cmd = [name] + args
    result = subprocess.run(cmd)
    return result.returncode


def search_tools(query: str):
    """Search available tools via apt-cache."""
    print(f"[fly] Searching for '{query}'...")
    subprocess.run(["apt-cache", "search", query])


def update_tools():
    """Update all fly-installed apt tools."""
    db = _load_db()
    apt_tools = [n for n, info in db.items() if info.get("method") == "apt"]

    if not apt_tools:
        print("[fly] No apt tools to update.")
        return

    print(f"[fly] Updating {len(apt_tools)} apt tools...")
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "--only-upgrade", "-y"] + apt_tools)
    print("[fly] ✓ Tools updated.")
