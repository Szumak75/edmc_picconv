# -*- coding: UTF-8 -*-
"""
Created on 04 mar 2019.

@author: szumak@virthost.pl
"""

from typing import List, Optional, Union

from jsktoolbox.attribtool import NoDynamicAttributes


class BMessages(NoDynamicAttributes):
    """MMessages metaclass.

    Container for list of messages
    """

    __messages: List[str] = None  # type: ignore

    def has_messages(self) -> bool:
        """Check if has messages."""
        return bool(self.__messages)

    @property
    def messages(self) -> List[str]:
        """Property for messages list."""
        try:
            self.__messages
        except NameError:
            self.__messages = []
        if self.__messages is None:
            self.__messages = []
        return self.__messages

    @messages.setter
    def messages(self, arg: Optional[Union[str, List]]) -> None:
        """Setter for messages list."""
        if arg is None or self.__messages is None:
            self.__messages = []
        if isinstance(arg, str):
            self.__messages.append(arg)
        elif isinstance(arg, List):
            for msg in arg:
                self.__messages.append(f"{msg}")
