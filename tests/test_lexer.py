"""Tests for the Fly lexer/transpiler"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fly.lexer import transpile_line, replace_keywords, transpile


def test_fn_to_def():
    assert "def hello():" in transpile_line("fn hello():")

def test_say_to_print():
    assert "print(" in transpile_line('say "hello"')

def test_let_removed():
    result = transpile_line("let x = 5")
    assert "let" not in result
    assert "x = 5" in result

def test_null_to_none():
    result = transpile_line("x = null")
    assert "None" in result

def test_true_false():
    result = transpile_line("let x = true")
    assert "True" in result

def test_use_to_import():
    result = transpile_line("use os")
    assert "import os" in result

def test_catch_to_except():
    result = transpile_line("catch Exception as e:")
    assert "except Exception as e:" in result

def test_string_preserved():
    """Keywords inside strings must not be replaced."""
    result = transpile_line('say "fn hello say null"')
    # print should be there, but "fn" and "null" inside string should be unchanged
    assert 'print' in result
    assert '"fn hello say null"' in result

def test_comment():
    result = transpile_line("## this is a comment")
    assert result.startswith("# this is a comment")

def test_full_transpile():
    code = """fn greet(name):
    say f"Hello {name}"
    return true
"""
    output = transpile(code)
    assert "def greet(name):" in output
    assert "print(" in output
    assert "return True" in output


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  [PASS] {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
