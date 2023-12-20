# -*- coding: UTF-8 -*-
"""
Created on 12 sep 2022.

@author: szumak@virthost.pl
"""

from picconv_libs.mclass import NoNewAttrs


class Raiser(NoNewAttrs):
    """Raiser class for returning formatted exceptions."""

    def message(self, class_name: str, currentframe, message="") -> str:
        """Return a formatted message string.

        class_name:     [str]   caller class name (self.__class__.__name__)
        currentframe:   [frame] inspect.currentframe()
        message:        [str]   message

        return: formated str
        """
        if message == "":
            return f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]"

        return f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]: {message}"

    def attribute_error(self, class_name, currentframe, message="") -> AttributeError:
        """Return AttributeError exception formatted string.

        class_name:     [str]   caller class name (self.__class__.__name__)
        currentframe:   [frame] inspect.currentframe()
        message:        [str]   message

        return: AttributeError
        """
        if message == "":
            return AttributeError(
                f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]"
            )

        return AttributeError(
            f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]: {message}"
        )

    def connection_error(self, class_name, currentframe, message="") -> ConnectionError:
        """Return ConnectionError exception formatted string.

        class_name:     [str]   caller class name (self.__class__.__name__)
        currentframe:   [frame] inspect.currentframe()
        message:        [str]   message

        return: ConnectionError
        """
        if message == "":
            return ConnectionError(
                f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]"
            )

        return ConnectionError(
            f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]: {message}"
        )

    def key_error(self, class_name, currentframe, message="") -> KeyError:
        """Return KeyError exception formatted string.

        class_name:     [str]   caller class name (self.__class__.__name__)
        currentframe:   [frame] inspect.currentframe()
        message:        [str]   message

        return: KeyError
        """
        if message == "":
            return KeyError(
                f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]"
            )

        return KeyError(
            f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]: {message}"
        )

    def os_error(self, class_name, currentframe, message="") -> OSError:
        """Return OSError exception formatted string.

        class_name:     [str]   caller class name (self.__class__.__name__)
        currentframe:   [frame] inspect.currentframe()
        message:        [str]   message

        return: OSError
        """
        if message == "":
            return OSError(
                f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]"
            )

        return OSError(
            f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]: {message}"
        )

    def syntax_error(self, class_name, currentframe, message="") -> SyntaxError:
        """Return SyntaxError exception formatted string.

        class_name:     [str]   caller class name (self.__class__.__name__)
        currentframe:   [frame] inspect.currentframe()
        message:        [str]   message

        return: SyntaxError
        """
        if message == "":
            return SyntaxError(
                f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]"
            )

        return SyntaxError(
            f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]: {message}"
        )

    def type_error(self, class_name, currentframe, message="") -> TypeError:
        """Return TypeError exception formatted string.

        class_name:     [str]   caller class name (self.__class__.__name__)
        currentframe:   [frame] inspect.currentframe()
        message:        [str]   message

        return: TypeError
        """
        if message == "":
            return TypeError(
                f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]"
            )

        return TypeError(
            f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]: {message}"
        )

    def value_error(self, class_name, currentframe, message="") -> ValueError:
        """Return ValueError exception formatted string.

        class_name:     [str]   caller class name (self.__class__.__name__)
        currentframe:   [frame] inspect.currentframe()
        message:        [str]   message

        return: ValueError
        """
        if message == "":
            return ValueError(
                f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]"
            )

        return ValueError(
            f"{class_name}.{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]: {message}"
        )
