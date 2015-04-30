Logging and Metrics
===================
This document describes the sites logging and metrics gathering functionality.The class
:class:`dfslog.classes.Logger` is used throughout the site to perform general logging and
gather metrics for the site. The enum class :class:`dfslog.classes.ErrorCodes` contains all of the
types of logging that could be used.

Logger
------

This class is used throughout the DFS site to allow for multiple logging capabilities for metrics and general
*Error Logging*.


.. autoclass:: dfslog.classes.Logger
    :members:
    :undoc-members:

Logger Error Codes
------------------
This enum is used to describe the error types.

.. autoclass:: dfslog.classes.ErrorCodes
    :members:
    :undoc-members:

Abstract Log
------------
The class :class:`dfslog.classes.AbstractLog`

.. autoclass:: dfslog.classes.AbstractLog
    :members:


Exceptions
----------
.. automodule:: dfslog.exceptions
    :members:
    :undoc-members:


Testing
-------
.. automodule:: dfslog.tests
    :members:
