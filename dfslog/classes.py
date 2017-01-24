from enum import Enum
from logging import getLogger

from dfslog.exceptions import ActionException
from dfslog.exceptions import ModelNotImplementedException
from dfslog.exceptions import ErrorCodeException
from dfslog.exceptions import LogMethodException
from dfslog.exceptions import MessageException

djangoLogger = getLogger('dfslog.classes')


class Logger:
    """
    Class for logging on the site
    """

    def __init__(self):
        pass

    @staticmethod
    def log(error_code, action, message, classes=[], **kwargs):
        """
        :param errorCode: This should use one of the predefined error codes listed in the class
            :class:`dfslog.logger.ErrorCodes`
        :param action: The action that is being performed for logging
        :param message: The message that would show up in the log file
        :param classes: the models that are included in the file
        :param kwargs: Additional arguments that we may use for Kiss Metrics
        """
        #
        # Validation of the error code to make sure the log
        # function was passed the ErrorCodes
        if not isinstance(error_code, ErrorCodes):
            raise ErrorCodeException()
        if not isinstance(action, str):
            raise ActionException()
        if not isinstance(message, str):
            raise MessageException()

        #
        # Validation to make sure all of the classes implement AbstractLog
        # message += " classes:"
        # for c in classes:
        #     if not isinstance(c, AbstractLog):
        #         raise ModelNotImplementedException(type(c).__name__)
        #     message +=" "+ c.log()

        log_string = "action: " + action + " message: " + message
        djangoLogger.info(log_string)


class ErrorCodes(Enum):
    """
    This class is an enum that describes all of the error codes.

    :ivar DEBUG: logs in the django DEBUG log
    :ivar INFO: logs in the django INFO log
    :ivar WARNING: logs in the django WARNING log
    :ivar ERROR: logs in the django ERROR log
    :ivar CRITICAL: logs in the django CRITICAL log
    :ivar METRICS: use this code if you wish to log the data as metrics. It will
        also log the data under the django INFO log.

    """
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    METRICS = 5


class AbstractLog():
    """
    This class should be implemented in any class or model that
    wants to be logged in the class :class:`dfslog.logger.Logger`'s
    method :func:`dfslog.logger.Logger.log`
    """

    def log(self):
        """
        This method must be implemented by any class that inherits
        this class. If not implemented the exception
        :class:`dfslog.exceptions.LogMethodException`
        will be thrown.
        :return: the string representation for logging purposes
        """
        raise LogMethodException(type(self).__name__)
