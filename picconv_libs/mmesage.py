# -*- coding: UTF-8 -*-
"""
Created on 04 mar 2019.

@author: szumak@virthost.pl

NoNewAttrs, no_new_attributes - Python Cookbook (2004), A. Martelli,
                                A. Ravenscroft, D. Ascher
"""

from picconv_libs.mclass import NoNewAttrs


class MMessages(NoNewAttrs):
    """MMessages metaclass.

    Container for list of messages
    """

    __messages = None

    def has_messages(self) -> bool:
        """Check if has messages."""
        return bool(self.__messages)

    @property
    def messages(self) -> list:
        """Property for messages list."""
        if self.__messages is None:
            self.__messages = []
        return self.__messages

    @messages.setter
    def messages(self, arg):
        """Setter for messages list."""
        if arg is None or self.__messages is None:
            self.__messages = []
        if isinstance(arg, str):
            self.__messages.append(arg)
        elif isinstance(arg, list):
            for msg in arg:
                self.__messages.append(f"{msg}")
