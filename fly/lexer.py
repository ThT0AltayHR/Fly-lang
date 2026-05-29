"""
Fly Language Lexer / Transpiler
Converts .fy source code to Python
"""

import re
from .keywords import FLY_TO_PYTHON


def transpile(source: str) -> str:
    """
    Transpile Fly source code to Python.
    Handles keyword mapping, string literals, and comments.
    """
    lines = source.split("\n")
    output_lines = []

    for line in lines:
        transpiled = transpile_line(line)
        output_lines.append(transpiled)

    python_code = "\n".join(output_lines)

    # Inject Fly builtins
    header = _build_header()
    return header + python_code


def transpile_line(line: str) -> str:
    """Transpile a single line."""
    # Preserve indentation
    stripped = line.lstrip()
    indent = line[: len(line) - len(stripped)]

    if not stripped:
        return line

    # Handle Fly-style comments: ## or # both work
    if stripped.startswith("##"):
        return indent + "#" + stripped[2:]

    # Replace keywords outside string literals
    result = replace_keywords(stripped)
    return indent + result


def replace_keywords(text: str) -> str:
    """Replace Fly keywords with Python equivalents, ignoring string contents."""
    # Tokenize: split into strings and non-strings
    parts = tokenize_strings(text)
    output = []

    for part_type, content in parts:
        if part_type == "string":
            output.append(content)
        else:
            # Apply keyword replacements on code segments
            replaced = _replace_in_code(content)
            output.append(replaced)

    return "".join(output)


def _replace_in_code(code: str) -> str:
    """Apply keyword replacements on a non-string code segment."""
    # Sort by length descending to avoid partial replacements
    sorted_kw = sorted(FLY_TO_PYTHON.items(), key=lambda x: -len(x[0]))

    for fly_kw, py_kw in sorted_kw:
        if not py_kw:
            # Keywords like let/const/var: remove the keyword but keep the rest
            pattern = r'\b' + re.escape(fly_kw) + r'\b\s*'
            code = re.sub(pattern, '', code)
        else:
            pattern = r'\b' + re.escape(fly_kw) + r'\b'
            code = re.sub(pattern, py_kw, code)

    return code


def tokenize_strings(text: str):
    """
    Split text into ('string', ...) and ('code', ...) parts.
    Handles single, double, triple-quoted strings.
    """
    parts = []
    i = 0
    n = len(text)

    while i < n:
        # Check for triple-quoted string
        if text[i:i+3] in ('"""', "'''"):
            quote = text[i:i+3]
            end = text.find(quote, i + 3)
            if end == -1:
                parts.append(("string", text[i:]))
                break
            end += 3
            parts.append(("string", text[i:end]))
            i = end
        # Check for single/double quoted string
        elif text[i] in ('"', "'"):
            quote = text[i]
            j = i + 1
            while j < n:
                if text[j] == '\\':
                    j += 2
                    continue
                if text[j] == quote:
                    j += 1
                    break
                j += 1
            parts.append(("string", text[i:j]))
            i = j
        # Check for comment
        elif text[i] == '#':
            parts.append(("string", text[i:]))
            break
        else:
            # Find next quote or end
            next_q = n
            for q in ('"', "'", '#'):
                idx = text.find(q, i)
                if idx != -1 and idx < next_q:
                    next_q = idx
            parts.append(("code", text[i:next_q]))
            i = next_q

    return parts


def _build_header() -> str:
    """Build the Python header injected at the top of every transpiled file."""
    return '''import sys as __sys__
import os as __os__
import subprocess as __subprocess__

def __fly_shell__(cmd, capture=False):
    """Execute a shell command."""
    if capture:
        result = __subprocess__.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    else:
        __subprocess__.run(cmd, shell=True)

def __fly_scan__(target, ports="1-1000", flags=""):
    """Quick nmap scan via Fly."""
    cmd = f"nmap {flags} -p {ports} {target}"
    __fly_shell__(cmd)

def __fly_recon__(domain):
    """Basic recon on a domain."""
    import socket
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] {domain} -> {ip}")
        return ip
    except Exception as e:
        print(f"[-] Recon failed: {e}")

def __fly_tool__(name, *args):
    """Run a Kali tool by name."""
    cmd = f"{name} {' '.join(str(a) for a in args)}"
    __fly_shell__(cmd)

def __fly_exploit__(*args, **kwargs):
    """Placeholder for exploit modules."""
    print("[fly] exploit() called - implement your exploit logic here")

def __fly_target__(host):
    """Set and return a target."""
    print(f"[fly] Target set: {host}")
    return host

'''
