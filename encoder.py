"""Implementation of JSONEncoder
"""
import re

try:
    from _json import encode_basestring_ascii as c_encode_basestring_ascii
except ImportError:
    c_encode_basestring_ascii = None
try:
    from _json import encode_basestring as c_encode_basestring
except ImportError:
    c_encode_basestring = None
try:
    from _json import make_encoder as c_make_encoder
except ImportError:
    c_make_encoder = None

ESCAPE = re.compile(r'[\x00-\x1f\\"\b\f\n\r\t]')
ESCAPE_ASCII = re.compile(r'([\\"]|[^\ -~])')
HAS_UTF8 = re.compile(b'[\x80-\xff]')
ESCAPE_DCT = {
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}
for i in range(0x20):
    ESCAPE_DCT.setdefault(chr(i), '\\u{0:04x}'.format(i))
    #ESCAPE_DCT.setdefault(chr(i), '\\u%04x' % (i,))
del i

INFINITY = float('inf')

def py_encode_basestring(s):
    """Return a JSON representation of a Python string

    """
    def replace(match):
        return ESCAPE_DCT[match.group(0)]
    return '"' + ESCAPE.sub(replace, s) + '"'


encode_basestring = (c_encode_basestring or py_encode_basestring)


def py_encode_basestring_ascii(s):
    """Return an ASCII-only JSON representation of a Python string

    """
    def replace(match):
        s = match.group(0)
        try:
            return ESCAPE_DCT[s]
        except KeyError:
            n = ord(s)
            if n < 0x10000:
                return '\\u{0:04x}'.format(n)
                #return '\\u%04x' % (n,)
            else:
                # surrogate pair
                n -= 0x10000
                s1 = 0xd800 | ((n >> 10) & 0x3ff)
                s2 = 0xdc00 | (n & 0x3ff)
                return '\\u{0:04x}\\u{1:04x}'.format(s1, s2)
    return '"' + ESCAPE_ASCII.sub(replace, s) + '"'


encode_basestring_ascii = (
    c_encode_basestring_ascii or py_encode_basestring_ascii)

class PYSONEncoder(object):
    """
    """
    item_sep = ', '
    key_sep = ': '
    def __init__(self, *, skipkeys=False, ensure_ascii=True,
            check_circular=True, allow_nan=True, sort_keys=False,
            indent=None, separators=None, default=None):
        """Constructor for PYSONEncoder
        """

        self.skipkeys = skipkeys
        self.ensure_ascii = ensure_ascii
        self.check_circular = check_circular
        self.allow_nan = allow_nan
        self.sort_keys = sort_keys
        self.indent = indent
        if separators is not None:
            self.item_separator, self.key_separator = separators
        elif indent is not None:
            self.item_separator = ','
        if default is not None:
            self.default = default

    def error(self, obj):
        """Implement this method in a subclass such that it returns
        a serializable object for ``obj``, or calls the base implementation
        (to raise a ``TypeError``).

        """
        raise TypeError(f'Object of type {obj.__class__.__name__} '
                        f'is not JSON serializable') 

    def encode(self, obj):
        """Return a JSON string representation of a Python data structure.

        >>> from .encoder import PYSONEncoder
        >>> PYSONEncoder().encode({"titles": ["Never", "Gonna", "Give", "You", "Up"]})
        '{"titles": ["Never", "Gonna", "Give", "You", "Up"]}'

        """
        # This is for extremely simple cases and benchmarks.
        if isinstance(obj, str):
            if self.ensure_ascii:
                return encode_basestring_ascii(obj)
            else:
                return encode_basestring(obj)
            
        # This doesn't pass the iterator directly to ''.join() because the
        # exceptions aren't as detailed.  The list call should be roughly
        # equivalent to the PySequence_Fast that ''.join() would do.
        chunks = self.iterencode(obj, _one_shot=True)
        if not isinstance(chunks, (list, tuple)):
            chunks = list(chunks)
        return ''.join(chunks)