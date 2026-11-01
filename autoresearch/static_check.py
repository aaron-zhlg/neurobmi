"""Static checks a candidate must pass before it is run on subject data.

This is defence in depth, not a sandbox: the harness also runs candidates in a
child process whose output never reaches an LLM. The checks block the obvious
ways a candidate could read files, reach the OS, or escape through dunders.
"""

from __future__ import annotations

import ast
from pathlib import Path

ALLOWED_IMPORT_ROOTS = {
    "numpy", "scipy", "sklearn", "math", "warnings", "itertools", "functools",
    "dataclasses", "typing", "collections", "__future__",
}
BANNED_CALLS = {
    "open", "exec", "eval", "compile", "__import__", "globals", "locals", "vars",
    "getattr", "setattr", "delattr", "input", "breakpoint", "memoryview",
}
# numpy / sklearn entry points that read or write files or fetch data.
BANNED_ATTRIBUTES = {
    "load", "loadtxt", "genfromtxt", "fromfile", "save", "savez", "savez_compressed", "savetxt",
    "tofile", "memmap", "DataSource", "fetch_openml", "load_svmlight_file", "dump_svmlight_file",
    "read_csv", "system", "popen",
}
REQUIRED_FUNCTION = "fit_predict"


def _looks_like_path(text: str) -> bool:
    token = text.strip()
    if token.endswith((".csv", ".npy", ".npz", ".json", ".txt", ".pkl", ".xlsx")):
        return True
    return not any(c.isspace() for c in token) and ("/" in token or "\\" in token or token.startswith("~"))


def check_source(source: str) -> list[str]:
    """Return a list of violations (empty means the candidate may run)."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [f"SyntaxError: line {exc.lineno}: {exc.msg}"]
    problems: list[str] = []
    for node in ast.walk(tree):
        line = getattr(node, "lineno", "?")
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] not in ALLOWED_IMPORT_ROOTS:
                    problems.append(f"line {line}: import of {alias.name!r} is not allowed")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if node.level or root not in ALLOWED_IMPORT_ROOTS:
                problems.append(f"line {line}: import from {node.module!r} is not allowed")
            if root == "sklearn" and (node.module or "").startswith("sklearn.datasets"):
                problems.append(f"line {line}: sklearn.datasets is not allowed")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in BANNED_CALLS:
            problems.append(f"line {line}: call to {node.func.id}() is not allowed")
        elif isinstance(node, ast.Name) and node.id in {"__builtins__", "__loader__", "__spec__", "__file__"}:
            problems.append(f"line {line}: access to {node.id} is not allowed")
        elif isinstance(node, ast.Attribute):
            if node.attr.startswith("__") and node.attr.endswith("__"):
                problems.append(f"line {line}: dunder attribute .{node.attr} is not allowed")
            elif node.attr in BANNED_ATTRIBUTES:
                problems.append(f"line {line}: attribute .{node.attr} (file / OS access) is not allowed")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and _looks_like_path(node.value):
            problems.append(f"line {line}: string literal that looks like a path is not allowed")
    if not any(isinstance(n, ast.FunctionDef) and n.name == REQUIRED_FUNCTION for n in tree.body):
        problems.append(f"candidate must define a top-level function {REQUIRED_FUNCTION}(train, test)")
    return problems


def check_file(path: Path) -> list[str]:
    return check_source(path.read_text(encoding="utf-8"))
