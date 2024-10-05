# -*- coding: UTF-8 -*-
"""
Created on 04 mar 2019.

@author: szumak@virthost.pl
"""

from typing import List, Optional, Union

from edpc.jsktoolbox.basetool.data import BData
from edpc.keys import EDPCKeys


class BMessages(BData):
    """MMessages metaclass.

    Container for list of messages
    """

    def has_messages(self) -> bool:
        """Check if has messages."""
        return bool(self._get_data(key=EDPCKeys.MESSAGES, default_value=[]))

    @property
    def messages(self) -> List[str]:
        """Property for messages list."""
        return self._get_data(key=EDPCKeys.MESSAGES, default_value=[])  # type: ignore

    @messages.setter
    def messages(self, arg: Optional[Union[str, List]]) -> None:
        """Setter for messages list."""
        if (
            arg is None
            or self._get_data(key=EDPCKeys.MESSAGES, default_value=None) is None
        ):
            self._set_data(key=EDPCKeys.MESSAGES, set_default_type=List, value=[])
        if isinstance(arg, str):
            self._get_data(key=EDPCKeys.MESSAGES).append(arg)  # type: ignore
        elif isinstance(arg, List):
            for msg in arg:
                self._get_data(key=EDPCKeys.MESSAGES).append(f"{msg}")  # type: ignore
