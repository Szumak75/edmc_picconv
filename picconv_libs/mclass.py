# -*- coding: UTF-8 -*-
"""
Created on 04 mar 2019.

@author: szumak@virthost.pl

NoNewAttrs, no_new_attributes - Python Cookbook (2004), A. Martelli,
                                A. Ravenscroft, D. Ascher
"""


def no_new_attributes(wrapped_setattr):
    """Raise an error when trying to add a new attribute.

    Allows to set new values for existing attributes.
    """

    def __setattr__(self, name, value):
        if hasattr(self, name):
            wrapped_setattr(self, name, value)
        else:
            raise AttributeError(f"Cannot add attribute {name} to {self}")

    return __setattr__


class NoNewAttrs:
    """Restrict the ability to dynamically define attributes."""

    __setattr__ = no_new_attributes(object.__setattr__)

    class __metaclass__(type):
        """Simple custom metaclass to block adding new attributes to this class."""

        __setattr__ = no_new_attributes(type.__setattr__)
