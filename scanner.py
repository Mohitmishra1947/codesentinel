import os

SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules"}


def find_python_files(path: str) -> list[str]:
    """Return .py files for a single file or a whole folder."""
    if os.path.isfile(path):
        return [path] if path.endswith(".py") else []

    files = []
    for root, dirs, names in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in names:
            if name.endswith(".py"):
                files.append(os.path.join(root, name))
    return files