import sys

PY3 = sys.version_info[0] >= 3

if PY3: # pragma NO COVER
    def _u(s):
        return s
else:
    def _u(s):
        return unicode(s, 'unicode_escape')
