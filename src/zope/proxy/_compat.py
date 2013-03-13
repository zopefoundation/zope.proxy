import platform
import sys

PY3 = sys.version_info[0] >= 3
py_impl = getattr(platform, 'python_implementation', lambda: None)
PYPY = py_impl() == 'PyPy'

