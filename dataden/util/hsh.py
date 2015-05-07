#
# dataden/hsh.py

import json
import hashlib

class InvalidArgumentException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__( "Invalid argument.")

class ObjectNotHashableException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__( "Object is not hashable.")

class InvalidCryptoException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__( "Could not generate hash for this crypto.")

class Hashable(object):
    """

    """
    def __init__(self, obj, crypto='sha256'):
        if not obj:
            raise InvalidArgumentException(self.__class__.__name__, '"obj" argument')

        self.crypto     = crypto
        self.encoding   = 'utf-8'

        try:
            self.s          = str( json.dumps( obj ).encode( self.encoding ) )
        except TypeError:
            raise ObjectNotHashableException(self.__class__.__name__,
                             '"obj" couldnt be converted to a string')
        except AttributeError:
            raise ObjectNotHashableException(self.__class__.__name__,
                '"obj" converted to a string, but it must contain only UTF-8 characters!')

        try:
            self.__h = getattr(self, self.crypto)( self.s )
        except AttributeError:
            # it will raise AttributeError if the crypto does
            # not exist, because its trying to call the named function
            raise InvalidCryptoException(self.__class__.__name__,
                        '"crypto" arg "%s" is invalid' % self.crypto )

    def hsh(self):
        return self.__h

    def sha256(self, s):
        return hashlib.sha256(s.encode(self.encoding)).hexdigest()
