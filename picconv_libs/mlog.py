# -*- coding: UTF-8 -*-
"""
Created on 04 mar 2019.

@author: szumak@virthost.pl

NoNewAttrs, no_new_attributes - Python Cookbook (2004), A. Martelli,
                                A. Ravenscroft, D. Ascher
"""

from picconv_libs.mclass import NoNewAttrs


class MLogProcessor(NoNewAttrs):
    """MLogProcessor metaclass.

    Container for logger processor methods.
    """

    __logger_queue = None
    __log_processor_engine = None
    __thread_logger = None

    @property
    def thlog(self):
        """Give me thread logger handler."""
        return self.__thread_logger

    @thlog.setter
    def thlog(self, value):
        self.__thread_logger = value

    @property
    def qlog(self):
        """Give me access to queue handler."""
        return self.__logger_queue

    @qlog.setter
    def qlog(self, value):
        """Setter for logging queue."""
        self.__logger_queue = value

    @property
    def log_processor(self):
        """Give me handler for log processor."""
        return self.__log_processor_engine

    @log_processor.setter
    def log_processor(self, value):
        """Setter for log processor instance."""
        self.__log_processor_engine = value


class MLogClient(NoNewAttrs):
    """MLogClass metaclass.

    Container for logger methods.
    """

    __logger = None

    @property
    def logger(self):
        """Give me logger handler."""
        return self.__logger

    @logger.setter
    def logger(self, arg):
        """Set logger instance."""
        self.__logger = arg
