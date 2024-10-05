# -*- coding: utf-8 -*-
"""
  keys.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 5.10.2024, 13:10:20
  
  Purpose: 
"""

from edpc.jsktoolbox.attribtool import ReadOnlyClass


class EDPCKeys(object, metaclass=ReadOnlyClass):
    """Keys for EDPC"""

    MESSAGES: str = "__messages__"


# #[EOF]#######################################################################
