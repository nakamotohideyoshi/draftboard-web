import unittest
from dfslog.logger import AbstractLog
from dfslog.exceptions import LogMethodException
from dfslog.logger import Logger
from dfslog.exceptions import  ErrorCodeException
from dfslog.exceptions import ActionException
from dfslog.exceptions import MessageException
from dfslog.logger import ErrorCodes
from dfslog.logger import ModelNotImplementedException

class AbstractLogTest( unittest.TestCase ):
    """
    Tests the :class:`dfslog.logger.AbstractLog` class
    """
    def test_log_method_not_implemented(self):
        """
        Tests to verify that the exception is thrown when
        log is called on a class that implements
        :class:`dfslog.logger.AbstractLog` but does not implement
        the log file.
        """

        class TestAbstract( AbstractLog ):
            pass


        test = TestAbstract()
        self.assertRaises(LogMethodException, lambda: test.log())


    def test_log_method_implemented(self):
        """
        Tests that the log file is properly implemented. The log method
        should return a string.
        """
        stringVal = "This is proper log return value"
        class TestAbstract( AbstractLog ):
            def log(self):
                return stringVal

        test = TestAbstract()
        self.assertEquals(test.log(), stringVal)


class LoggerTest( unittest.TestCase):
    """
    Tests the :class:`dfslog.logger.Logger` class.
    """

    def test_invalid_arguments_log_method(self):
        """
        Tests to make sure all of the Exceptions are called properly
        when the log method is used wrong.
        """
        class TestProperAbstract( AbstractLog ):
            def log(self):
                return "Test 1"
        class TestUnimplementedAbstract(  ):
            def log(self):
                return "Test 1"
        class TestUnimplementedLog( AbstractLog ):
            pass

        logger = Logger()
        self.assertRaises(ErrorCodeException, lambda: logger.log(0, "someAction", "someMessage"))
        self.assertRaises(ActionException, lambda: logger.log(ErrorCodes.DEBUG, 0, "someMessage"))
        self.assertRaises(MessageException, lambda: logger.log(ErrorCodes.CRITICAL, "someAction", 0))
        self.assertRaises(ModelNotImplementedException, lambda: \
                    logger.log(ErrorCodes.CRITICAL, "someAction", "someMessage", \
                               [TestProperAbstract(), TestUnimplementedAbstract()]))
        self.assertRaises(LogMethodException, lambda: \
                    logger.log(ErrorCodes.CRITICAL, "someAction", "someMessage", \
                               [TestProperAbstract(), TestUnimplementedLog()]))

