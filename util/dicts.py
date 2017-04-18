from collections import Counter
from functools import reduce
from logging import getLogger

logger = getLogger('util.dicts')


# %cpaste
# class Dict2(dict):
#     class ValueDoesNotExist(Exception): pass
#     def get(self, field, *args, **kwargs):
#         val = super().get(field)
#         if val is None:
#             raise self.ValueDoesNotExist('lol %s wasnt there' % field)
#         return val
#
# --
# d2 = Dict2({'k':'v'})
# d2.get('k')
# d2.get('steve')

class DictTools:
    @staticmethod
    def combine(d1, d2):
        """
        values are merged and added together for matching keys.

        example usage:

            >>> d1 = {'a':234, 'b':1}
            >>> d2 = {'b':1, 'c':123}
            >>> d = DictTools.combine(d1, d2)
            >>> d
            Counter({'b': 2, 'c': 123, 'a': 234})
            >>>

        :param d1: the target dict
        :param d2: using the key-value pairs in d2, combine and add them to d1
        :return: Counter object - you can easily cast it to a dict if you wish with dict(Counter())
        """

        def update_in_place(a, b):
            a.update(b)
            return a

        return reduce(update_in_place, (Counter(d) for d in [d1, d2]))

    @staticmethod
    def subtract(d1, d2):
        """
        removes the entries in d2 from d1, and returns d1.

        the caller should make copies of d1 if they wish to preserve its original data

        :param d1:
        :param d2:
        :return:
        """

        for k in d2.keys():
            try:
                d1.pop(k)
            except KeyError:
                pass
        return d1


class Reducer(object):
    """
    Removes key-values from the top level of a dict,
     for all keys in the 'remove_fields' list.

    The primary goal of this class is to reduce the
    size of the dict by removing unwanted/unecessary key-values.
    """

    class InvalidDataType(Exception):
        pass

    class RemoveFieldsNotSetException(Exception):
        pass

    # inheriting classes should set this to a list of string field names to remove
    remove_fields = None

    str_true = "true"
    str_false = "false"
    str_bools = [str_true, str_false]

    def __init__(self, data):
        if not isinstance(data, dict):
            err_msg = '"data" must be of type: dict, not %s' % type(data)
            raise self.InvalidDataType(err_msg)
        self.data = data  # save the original data
        self.reduced = self.data.copy()  # clone the data coming in
        self.__validate_remove_fields(self.remove_fields)

    def __validate_remove_fields(self, remove_fields):
        if remove_fields is None:
            err_msg = '"remove_fields" list must be a list of key names'
            raise self.RemoveFieldsNotSetException(err_msg)

    def str2bool(self, val):
        """
        val can be any type.
            if val is a 'str' and (val == "true" or val == "false"):
                True, or False  (for "true" and "false", respectively) is returned
            else:
                val is returned as-is/unchanged

        """
        if not isinstance(val, str):
            return val

        if val == self.str_false:
            return False
        elif val == self.str_true:
            return True
        else:
            return False  # default !?

    def get_internal_data(self):
        return self.reduced

    def pre_reduce(self):
        """
        you should override this in child class if you want
        to do anything that happens immediately prior
        to the code in reduce() being executed
        """
        pass  # by default does nothing, side effects nothing

    def reduce(self):
        self.pre_reduce()

        # remove keys we dont care about, and return the internal data
        for field in self.remove_fields:
            try:
                # this actually removes the fields from the dict!
                self.reduced.pop(field)
            except KeyError:
                # the key did not exist, but we dont care
                pass
        #
        return self.reduced


class Shrinker(object):
    """
    Shrinker is meant to be subclassed and have its 'fields' set, ie:

        >>> class MyShrinker(Shrinker):
        ...     fields = { 'rename_this_key' : 'new_name' }

    Renames keys at the top of level of this object (ie: it shrinks them).
    """

    class FieldsNotSetException(Exception):
        pass

    # child classes must set a dict of the key:value pairs
    # that define the renamings. for example, setting 'fields':
    #
    #      fields = { 'some_key' : 'sk' }
    #
    # and calling the shrink() method will return a new dict
    # in which the key "some_key" has been renamed to "sk"
    fields = None

    def __init__(self, data):
        self.data = data
        self.shrunk = None
        self.__validate_fields(self.fields)

    def shrink(self):
        """ return shrunk data """
        self.shrunk = self.data.copy()
        for old_field, new_field in self.fields.items():
            # print(self.__class__.__name__, 'old_field', old_field, 'new_field', new_field)
            if new_field in self.shrunk:
                # prevent us from remapping a key
                # to a keyname that already exists
                # print('    new_field already exists:', new_field)
                continue

            try:
                val = self.shrunk.pop(old_field)
            except KeyError:
                # print('    old_field does not exist:', old_field)
                continue  # old_field didnt exist. dont hold it against them

            # if val is None:
            #     print('    old_field pop()ed value:', str(val))
            #     continue # dont add a random default value if the field doesnt exist

            # print('    remapping old_field[%s] to { "%s" : "%s" }' % (
            # old_field, new_field, str(val)))
            self.shrunk[new_field] = val
        #
        return self.shrunk

    def __validate_fields(self, fields):
        if fields is None:
            err_msg = '"fields" must be set to a dict of key renamings!'
            raise self.FieldsNotSetException(err_msg)


class Manager(object):
    # exceptions for validity checking
    class InvalidReducer(Exception):
        pass

    class InvalidShrinker(Exception):
        pass

    # must be set by child classes
    reducer_class = None
    shrinker_class = None

    str_true = "true"
    str_false = "false"
    str_bools = [str_true, str_false]

    def __init__(self, raw_data):
        """
        adds the key values in the 'stats' dict into the
        """
        if self.reducer_class is None:
            raise self.InvalidReducer('"reducer_class" cant be None')
        if self.shrinker_class is None:
            raise self.InvalidShrinker('"shrinker_class" cant be None')

        if raw_data is None:
            logger.warning("raw_data is None - %s" % self.__class__.__name__)
            raw_data = {}
        self.raw_data = raw_data

    @staticmethod
    def int2bool(val):
        """ takes str2bool a step further and turns """

        # convert floats to ints
        if isinstance(val, float):
            val = int(val)

        if not isinstance(val, int):
            return val  # could raise here... idk

        return val == 1

    def str2bool(self, val):
        """ guess what this method does. you got it. """
        if not isinstance(val, str):
            return val

        if val == self.str_false:
            return False
        elif val == self.str_true:
            return True
        else:
            return False  # default !?

    def get_data(self, additional_data=None):
        # reduce the raw data - pop() unwanted fields
        reduced = self.reducer_class(self.raw_data).reduce()
        # shrink the reduced data
        shrunk = self.shrinker_class(reduced).shrink()

        # add_data should be called after
        return self.add_data(shrunk, additional_data)

    @staticmethod
    def add_data(base_data, additional=None):
        if additional is not None:
            for k, v in additional.items():
                # add this key:value of additional data,
                # but only if the field doesnt exist already in orig
                if base_data.get(k, None) is None:
                    base_data[k] = v
        return base_data
