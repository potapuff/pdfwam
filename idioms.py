# -- coding: utf-8
""" Pythonic idioms """

from contextlib import contextmanager

___author__ = "Anand B Pillai"
__maintainer__ = "Anand B Pillai"
__version__ = "0.1"
__lastmodified__ = "2013-03-24 14:07:21 IST"

# Ignore exceptions
class ignore(object):
    """ Context manager class for ignoring exceptions
    generated in the dependent block.

    >>> x='python'
    >>> try:
    ...     x.index('.')
    ... except ValueError, e:
    ...     print e
    ... 
    substring not found
    >>> with ignore():
    ...     x.index('.')
    ... 
    """
    
    def __enter__(self):
        pass
    
    def __exit__(self, type, value, traceback):
        # According to PEP 343 returning True from
        # __exit__ causes the context manager to ignore
        # exceptions generated in the BLOCK.
        return True

@contextmanager
def ignored(*exceptions):
    """ Ignore specific chain of exceptions

    >>> import os
    >>> with ignored(OSError):
    ...     os.remove('notfound')
    ... 
    >>> 
    """

    try:
        yield
    except exceptions:
        pass
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()

