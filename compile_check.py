"""Script to compile all Python files and report syntax errors."""
import os, sys

failures = []
for root, dirs, files in os.walk('.'):
    # Skip virtual env and cache
    if '.venv' in dirs:
        dirs.remove('.venv')
    if '__pycache__' in dirs:
        dirs.remove('__pycache__')
    for filename in files:
        if not filename.endswith('.py'):
            continue
        path = os.path.join(root, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                source = f.read()
            compile(source, path, 'exec')
        except Exception as e:
            print(f"Failed to compile {path}: {e}")
            failures.append(path)
if failures:
    sys.exit(1)
sys.exit(0)