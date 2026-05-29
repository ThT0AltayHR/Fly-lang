"""
Fly Language Keyword Mappings
Maps Fly keywords to Python equivalents
"""

FLY_TO_PYTHON = {
    # Functions & Classes
    "fn":           "def",
    "class":        "class",
    "init":         "__init__",
    "self":         "self",
    "return":       "return",
    "yield":        "yield",
    "lambda":       "lambda",
    "async":        "async",
    "await":        "await",

    # Control Flow
    "if":           "if",
    "elif":         "elif",
    "else":         "else",
    "for":          "for",
    "while":        "while",
    "break":        "break",
    "continue":     "continue",
    "pass":         "pass",
    "match":        "match",
    "case":         "case",

    # Output / Input
    "say":          "print",
    "ask":          "input",
    "log":          "print",
    "err":          "sys.stderr.write",

    # Imports
    "use":          "import",
    "from":         "from",
    "as":           "as",

    # Exceptions
    "try":          "try",
    "catch":        "except",
    "finally":      "finally",
    "raise":        "raise",
    "throw":        "raise",

    # Boolean / Null
    "true":         "True",
    "false":        "False",
    "null":         "None",
    "none":         "None",
    "and":          "and",
    "or":           "or",
    "not":          "not",
    "in":           "in",
    "is":           "is",

    # Variables
    "let":          "",
    "const":        "",
    "var":          "",

    # Context Managers
    "with":         "with",
    "open":         "open",

    # Delete / Assert
    "delete":       "del",
    "assert":       "assert",

    # Global / Nonlocal
    "global":       "global",
    "nonlocal":     "nonlocal",

    # Type Checking
    "typeof":       "type",
    "isinstance":   "isinstance",

    # Fly-specific
    "scan":         "__fly_scan__",
    "exploit":      "__fly_exploit__",
    "recon":        "__fly_recon__",
    "shell":        "__fly_shell__",
    "tool":         "__fly_tool__",
    "target":       "__fly_target__",
}

PYTHON_KEYWORDS = set(FLY_TO_PYTHON.values())
FLY_KEYWORDS = set(FLY_TO_PYTHON.keys())
