"""General independent utilities"""


import datetime
import re
from typing import Union

ALPHANUMERICS_RE = re.compile(r'([^\s\w])+')


def has_unicode(text):
    """Python 2.7 compatible method to check if text has non-encoded
    unicode in it

    Args:
        text (str or unicode)

    Usage:
        >>> has_unicode("Hello world!")
        False
        >>> has_unicode("👋 🌎 !")
        True
    """
    return not all(ord(char) < 128 for char in text)


def chunks(seq, chunk_size):
    """Returns a generator which yields contiguous chunks of the sequence
    of size (up to) `chunk_size`.

    Usage:
        >>> list(chunk([1,2,3,4], 2))
        [[1, 2], [3, 4]]
        >>> list(chunk([1,2,3,4,5], 2))
        [[1, 2], [3, 4], [5]]
    """

    def take(seq, n):
        for i in range(n):
            try:
                yield next(seq)
            except StopIteration:
                return

    if not hasattr(seq, 'next'):
        seq = iter(seq)
    while True:
        x = list(take(seq, chunk_size))
        if x:
            yield x
        else:
            break


def rm_punctuation(text):
    """Strips anything that is not an alphanumeric or space"""
    return ALPHANUMERICS_RE.sub('', text)


def parse_datetime(value):
    """Parses ISO datetime formatted string.::
    >>> parse_datetime("2009-01-02T03:04:05.006789")
    datetime.datetime(2009, 1, 2, 3, 4, 5, 6789)
    """
    if isinstance(value, datetime.datetime):
        return value
    else:
        tokens = re.split(r'-|T|:|\.| ', value)
        return datetime.datetime(*map(int, tokens))


def merge_unique_lists(lists, hash_fn=None):
    """Combine unique lists into a new unique list. Preserves ordering."""
    result = []
    seen = set()
    for lst in lists:
        for el in lst:
            hsh = hash_fn(el) if hash_fn else el
            if hsh not in seen:
                result.append(el)
                seen.add(hsh)
    return result


def get_text_value(text):
    """Returns the text value from a property that can either be a properly
    formed /type/text object, or a (incorrect) string.
    Used for Work/Edition 'notes' and 'description' and Author 'bio'.
    """
    try:
        return text.get('value')
    except AttributeError:
        return text


def extract_olid_from_url(url, url_type):
    """No single field has the match's OpenLibrary ID in isolation so we
    extract it from the info_url field.

    Args:
        url_type (unicode) - "books", "authors", "works", etc
                             which are found in the ol url, e.g.:
                             openlibrary.org/books/...

    Returns:
        olid (unicode)

    Usage:
        >>> url = u'https://openlibrary.org/books/OL25943366M'
        >>> _extract_olid_from_url(url, u"books")
            u"OL25943366M"
    """
    ol_url_pattern = r'[/]%s[/]([0-9a-zA-Z]+)' % url_type
    try:
        return re.search(ol_url_pattern, url).group(1)
    except AttributeError:
        return None  # No match


def get_approval_from_cli(message: str) -> bool:
    return input(message).strip().lower() in ('y', 'yes')
