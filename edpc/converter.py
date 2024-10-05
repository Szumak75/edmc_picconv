# -*- coding: UTF-8 -*-
"""
Created on 30 dec 2022.

@author: szumak@virthost.pl
"""

from inspect import currentframe
import os
import shutil
import time
import tkinter as tk
from datetime import datetime, timedelta
from queue import Queue, SimpleQueue
from typing import Optional, Union

from PIL import Image

from edpc.jsktoolbox.raisetool import Raise
from edpc.base_log import BLogClient
from edpc.base_message import BMessages
from edpc.system import Directory, LogClient
from edpc.keys import EDPCKeys


class PicConverter(BLogClient, BMessages):
    """PicConverter class for ED Screenshots."""

    # {
    # "timestamp":"2022-12-30T23:33:56Z",
    # "event":"Screenshot",
    # "Filename":"\\ED_Pictures\\Screenshot_0029.bmp",
    # "Width":1600,
    # "Height":900,
    # "System":"Plaa Thua MS-Y b56-0",
    # "Body":"Plaa Thua MS-Y b56-0 1 a"
    # }

    def __init__(self, queue: Union[Queue, SimpleQueue]) -> None:
        """Initialize PicConverter class."""
        self._set_data(
            key=EDPCKeys.DST_DIR, value=None, set_default_type=Optional[Directory]
        )
        self._set_data(
            key=EDPCKeys.SRC_DIR, value=None, set_default_type=Optional[Directory]
        )
        self._set_data(key=EDPCKeys.SUFFIX, value="bmp", set_default_type=str)
        self._set_data(key=EDPCKeys.REMOVE, value=True, set_default_type=bool)
        self._set_data(
            key=EDPCKeys.DELTA_TIME, value=None, set_default_type=Optional[timedelta]
        )
        self._set_data(key=EDPCKeys.CONVERT_TYPE, value=False, set_default_type=bool)

        self.src_dir = Directory()
        self.dst_dir = Directory()
        self._set_data(
            key=EDPCKeys.LOG_TIME, value="%Y-%m-%dT%H:%M:%SZ", set_default_type=str
        )
        self._set_data(
            key=EDPCKeys.PIC_TIME,
            value="%Y%m%d-%H%M%S",
            set_default_type=str,
        )
        self._set_data(
            key=EDPCKeys.PIC_FILE,
            value="{} {}.{}",
            set_default_type=str,
        )
        self._set_data(
            key=EDPCKeys.PIC_COUNT_FILE, value="{} {} ({:02d}).{}", set_default_type=str
        )

        self._set_data(
            key=EDPCKeys.DELTA_TIME,
            value=datetime(3309, 1, 1, 1, 1, 43) - datetime(2023, 1, 1, 2, 1, 43),
        )

        # init log subsystem
        if not isinstance(queue, (Queue, SimpleQueue)):
            raise Raise.error(
                f"Queue or SimpleQueue type expected, '{type(queue)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self.logger = LogClient(queue)

    @property
    def remove(self) -> bool:
        """Give me decision to remove source file after conversion."""
        return self._get_data(EDPCKeys.REMOVE)  # type: ignore

    @remove.setter
    def remove(self, arg: Union[bool, int, tk.IntVar]) -> None:
        if isinstance(arg, bool):
            self._set_data(key=EDPCKeys.REMOVE, value=arg)
        elif isinstance(arg, int) and arg == 1:
            self._set_data(key=EDPCKeys.REMOVE, value=True)
        elif isinstance(arg, tk.IntVar) and arg.get() == 1:
            self._set_data(key=EDPCKeys.REMOVE, value=True)
        else:
            self._set_data(key=EDPCKeys.REMOVE, value=False)

    @property
    def convert_type(self) -> bool:
        """Give me decision to convert source file type."""
        return self._get_data(EDPCKeys.CONVERT_TYPE)  # type: ignore

    @convert_type.setter
    def convert_type(self, arg: Union[bool, int, tk.IntVar]) -> None:
        if isinstance(arg, bool):
            self._set_data(key=EDPCKeys.CONVERT_TYPE, value=arg)
        elif isinstance(arg, int) and arg == 1:
            self._set_data(key=EDPCKeys.CONVERT_TYPE, value=True)
        elif isinstance(arg, tk.IntVar) and arg.get() == 1:
            self._set_data(key=EDPCKeys.CONVERT_TYPE, value=True)
        else:
            self._set_data(key=EDPCKeys.CONVERT_TYPE, value=False)

    @property
    def src_dir(self) -> Directory:
        """Give me source directory with files to convert."""
        return self._get_data(key=EDPCKeys.SRC_DIR)  # type: ignore

    @src_dir.setter
    def src_dir(self, arg: Directory) -> None:
        self._set_data(key=EDPCKeys.SRC_DIR, value=arg)

    @property
    def dst_dir(self) -> Directory:
        """Give me destination directory for converted files."""
        return self._get_data(key=EDPCKeys.DST_DIR)  # type: ignore

    @dst_dir.setter
    def dst_dir(self, arg: Directory) -> None:
        self._set_data(key=EDPCKeys.DST_DIR, value=arg)

    @property
    def suffix(self) -> str:
        """Suffix for pic filename."""
        return self._get_data(key=EDPCKeys.SUFFIX)  # type: ignore

    @suffix.setter
    def suffix(self, arg: str) -> None:
        """Setter for suffix pic filename."""
        self._set_data(key=EDPCKeys.SUFFIX, value=arg)

    def str_time(self, arg: str) -> str:
        """Timestamp from logs in local time convert to game time string.

        input: 2023-01-01T03:01:43Z
        output: 33090101-010143
        """
        # create struct_time
        str_time: time.struct_time = time.strptime(arg, self._get_data(key=EDPCKeys.LOG_TIME))  # type: ignore

        # create datetime object
        dt_obj = datetime(*str_time[:6])

        # conversion local time to game time
        dt_obj2: datetime = dt_obj + self._get_data(key=EDPCKeys.DELTA_TIME)  # type: ignore

        return dt_obj2.strftime(self._get_data(key=EDPCKeys.PIC_TIME))  # type: ignore

    def convert(self, arg: dict) -> bool:
        """Pictures converter."""
        done: bool = False
        convert: bool = False

        local_suffix = os.path.splitext(arg[EDPCKeys.P_FILENAME])[1][1:]
        self.logger.debug = "def convert"
        self.logger.debug = f"Local suffix: {local_suffix}"
        self.logger.debug = f"Suffix: {self._get_data(key=EDPCKeys.SUFFIX)}"
        self.logger.debug = (
            f"Local convert flag: {self._get_data(key=EDPCKeys.CONVERT_TYPE)}"
        )
        if self._get_data(key=EDPCKeys.CONVERT_TYPE):
            local_suffix = self._get_data(key=EDPCKeys.SUFFIX)
            convert = True

        # check dirs
        if not Directory().is_directory(self.src_dir.dir):
            self.logger.error = f"Source directory is invalid: {self.src_dir.dir}"
            return done
        if not Directory().is_directory(self.dst_dir.dir):
            self.logger.error = f"Destination directory is invalid: {self.dst_dir.dir}"
            return done
        # check filename
        src: str = os.path.join(self.src_dir.dir, arg[EDPCKeys.P_FILENAME])
        if not os.path.exists(src):
            self.logger.error = f"Source file not found: {src}"
            return done
        # generate dst filename
        name = arg[EDPCKeys.P_BODY]
        dst: str = os.path.join(
            self.dst_dir.dir,
            self._get_data(key=EDPCKeys.PIC_FILE).format(  # type: ignore
                self.str_time(arg[EDPCKeys.P_TIMESTAMP]), name, local_suffix
            ),
        )
        # if dst file is present, generate new unique name
        count = 0
        while os.path.exists(dst):
            count += 1
            dst = os.path.join(
                self.dst_dir.dir,
                self._get_data(key=EDPCKeys.PIC_COUNT_FILE).format(  # type: ignore
                    self.str_time(arg[EDPCKeys.P_TIMESTAMP]), name, count, local_suffix
                ),
            )
            if count == 99:
                self.logger.error = "Cannot generate a valid filename"
                return done
        # save or convert file
        if convert:
            if self.__pil_convert(src, dst):
                done = True
            else:
                self.logger.error = "Cannot convert type of file, try to make copy..."
                if self.__copy_file(src, dst):
                    done = True
                else:
                    return done
        else:
            done = self.__copy_file(src, dst)
            if not done:
                return done
        # remove src
        try:
            if self.remove:
                self.logger.debug = (
                    f"try to remove file: {arg[EDPCKeys.P_FILENAME]}....."
                )
                os.remove(src)
                self.logger.debug = "... done"
        except Exception as ex:
            self.logger.error = f"ERROR: {ex.args[1]}"

        return done

    def __copy_file(self, src: str, dst: str) -> bool:
        """Copy file to new location."""
        # save file
        filename1: str = os.path.basename(src)
        filename2: str = os.path.basename(dst)
        try:
            self.logger.debug = f"try to copy file: {filename1} to: {filename2}....."
            shutil.copy(src, dst)
            self.messages = f"{filename2} copied"
            self.logger.debug = "... done"
            return True
        except Exception as ex:
            self.logger.error = f"ERROR: {ex.args[1]}"
        return False

    def __pil_convert(self, src: str, dst: str) -> bool:
        """Convert file to new type."""
        filename1: str = os.path.basename(src)
        filename2: str = os.path.basename(dst)
        self.logger.debug = f"SRC: {src}"
        self.logger.debug = f"DST: {dst}"
        try:
            self.logger.debug = f"try to convert file: {filename1} to: {filename2}....."
            img = Image.open(src)
            img.save(dst)
            self.messages = f"{filename2} converted"
            self.logger.debug = "... done"
            return True
        except Exception as ex:
            self.logger.error = f"ERROR: {ex.args[1]}"
        return False
