r"""

"""
__version__ = '1.0.0'
__all__ = [
    'convert_to_str', 'write_to_file', 
    'read_from_string', 'read_from_file',
    'PYSONDecoder', 'PYSONEncoder'
    # To-do, write function names
]

__author__ = 'Rauan Omirkul <ommirkulr@gmail.com>'

from .encoder import PYSONEncoder

_default_encoder = PYSONEncoder(
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    indent=None,
    separators=None,
    default=None,
)


def write_to_file(obj, fp, *, skipkeys=False, ensure_ascii=True, check_circular = True,
                  indent=None, separators=None, default = None,
                  sort_keys=False, cls=None, **kw):
    """Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    If ``skipkeys`` is true then ``dict`` keys that are not basic types
    (``str``, ``int``, ``float``, ``bool``, ``None``) will be skipped
    instead of raising a ``TypeError``.
    
    If ``ensure_ascii`` is false, then the strings written to ``fp`` can
    contain non-ASCII characters if they appear in strings contained in
    ``obj``. Otherwise, all such characters are escaped in JSON strings.

    If ``check_circular`` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``RecursionError`` (or worse).

    If ``indent`` is a non-negative integer, then JSON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. ``None`` is the most compact
    representation.

    If specified, ``separators`` should be an ``(item_separator, key_separator)``
    tuple.  The default is ``(', ', ': ')`` if *indent* is ``None`` and
    ``(',', ': ')`` otherwise.  To get the most compact JSON representation,
    you should specify ``(',', ':')`` to eliminate whitespace.

    If *sort_keys* is true (default: ``False``), then the output of
    dictionaries will be sorted by key.

    To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg; otherwise ``JSONEncoder`` is used.
    
    """
    if (not skipkeys and ensure_ascii and
        check_circular and cls is None and
        indent is None and separators is None and
        default is None and not sort_keys and not kw):
        iterable = _default_encoder.encode(obj)
    else:
        if cls is None:
            cls = PYSONEncoder
        iterable = cls(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
            check_circular=check_circular, indent=indent,
            separators=separators,
            default=default, sort_keys=sort_keys, **kw).encode(obj)
    
    for chunk in iterable:
        fp.write(chunk)
    

def convert_to_str():
    """
    """

def read_from_string():
    """
    """

def read_from_file():
    """
    """