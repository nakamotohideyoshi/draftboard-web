#
# decorators.py

from contextlib import ContextDecorator
from rest_framework.exceptions import APIException

class remap_exception(ContextDecorator):
    """
    example usage:

    In [67]: class RemappedException(Exception): pass
    In [68]: class SpecialException(Exception): pass
    In [69]: @remap_exception(RemappedException)
       ....: def fn():
       ....:         print('in fn() about to raise SpecialException')
       ....:         raise SpecialException('oh nos!')
       ....:

    In [70]: fn() # doesnt raise SpecialException because of decorator remapping!

    in __exit__(self, exc_type, exc, exc_tb)
         22         new_exception = self.exception_class(exc) # pass the message
         23         #new_exception.status_code = 405
    ---> 24         raise new_exception

    RemappedException: oh nos!           # <-- note the decorator remapped exception is raised instead


    """
    def __init__(self, exception_class):
        self.exception_class = exception_class
        self.exc_type = None
        self.exc = None
        self.exc_tb = None
    def __enter__(self):
        print('__enter__')
        print('remap to exception class:', str(self.exception_class))
        pass
    def __exit__(self, exc_type, exc, exc_tb):
        print('exc_type:', exc_type)
        print('exc:', exc)
        print('exc_tb:', exc_tb)
        self.exc_type = exc_type
        self.exc = exc
        self.exc_tb = exc_tb
        print('__exit__')
        new_exception = self.exception_class(exc) # pass the message
        #new_exception.status_code = 405
        raise new_exception

class api_exception(ContextDecorator):
    """
    In [73]: class NonAPIException(Exception): pass
    In [74]: @api_exception(APIException)
       ....: def fn():
       ....:         print('in fn() about to raise NonAPIException')
       ....:         raise NonAPIException('oh nos!')
       ....:

    In [75]: fn()
    ---------------------------------------------------------------------------
    NonAPIException                           Traceback (most recent call last)
    /usr/lib/python3.4/contextlib.py in inner(*args, **kwds)
         29             with self._recreate_cm():
    ---> 30                 return func(*args, **kwds)
         31         return inner

    <ipython-input-74-4d6542e119c9> in fn()
          3         print('in fn() about to raise NonAPIException')
    ----> 4         raise NonAPIException('oh nos!')
          5

    NonAPIException: oh nos!

    During handling of the above exception, another exception occurred:

    APIException                              Traceback (most recent call last)
    <ipython-input-75-fd7064640434> in <module>()
    ----> 1 fn()

    /usr/lib/python3.4/contextlib.py in inner(*args, **kwds)
         28         def inner(*args, **kwds):
         29             with self._recreate_cm():
    ---> 30                 return func(*args, **kwds)
         31         return inner
         32

    <ipython-input-71-bacde311bdbe> in __exit__(self, exc_type, exc, exc_tb)
         16         new_exception = self.exception_class(exc) # pass the message
         17         new_exception.status_code = self.status_code
    ---> 18         raise new_exception

    APIException: oh nos!
    """
    def __init__(self, exception_class=None, status_code=None):
        self.exception_class = exception_class
        if self.exception_class is None:
            self.exception_class = APIException
        self.status_code = status_code
        if self.status_code is None:
            self.status_code = 405
    def __enter__(self):
        #print('remap to exception class:', str(self.exception_class))
        pass
    def __exit__(self, exc_type, exc, exc_tb):
        #print('__exit__')
        new_exception = self.exception_class(exc) # pass the message
        new_exception.status_code = self.status_code
        raise new_exception
