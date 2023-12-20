# -*- coding: UTF-8 -*-
"""
Created on 30 dec 2022.

@author: szumak@virthost.pl
"""

import importlib
import inspect
import os
import shutil
import time
import tkinter as tk
from datetime import datetime  # , timedelta
from queue import Queue, SimpleQueue

from picconv_libs.mclass import NoNewAttrs
from picconv_libs.mlog import MLogClient
from picconv_libs.mmesage import MMessages
from picconv_libs.mraise import Raiser
from picconv_libs.system import Directory, LogClient


class PicConverter(MLogClient, MMessages, NoNewAttrs):
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

    __templates = None
    __vars = None

    def __init__(self, queue: Queue or SimpleQueue):
        """Initialize PicConverter class."""
        self.__vars = {
            "srcdir": None,
            "dstdir": None,
            "suffix": "bmp",
            "remove": True,
            "timedelta": None,
            "pillow": False,
            "converttype": False,
            "pillib": None,
        }
        self.srcdir = Directory()
        self.dstdir = Directory()
        self.__templates = {
            "logtime": "%Y-%m-%dT%H:%M:%SZ",
            "pictime": "%Y%m%d-%H%M%S",
            "picfile": "{} {}.{}",
            "piccountfile": "{} {} ({:02d}).{}",
        }
        self.__vars["timedelta"] = datetime(3309, 1, 1, 1, 1, 43) - datetime(
            2023, 1, 1, 2, 1, 43
        )

        # init log subsystem
        if isinstance(queue, (Queue, SimpleQueue)):
            self.logger = LogClient(queue)
        else:
            raise Raiser().type_error(
                self.__class__.__name__,
                inspect.currentframe(),
                f"Queue or SimpleQueue type expected, '{type(queue)}' received.",
            )

    @property
    def remove(self):
        """Give me decision to remove source file after convertion."""
        return self.__vars["remove"]

    @remove.setter
    def remove(self, arg):
        if isinstance(arg, bool):
            self.__vars["remove"] = arg
        elif isinstance(arg, int) and arg == 1:
            self.__vars["remove"] = True
        elif isinstance(arg, tk.IntVar) and arg.get() == 1:
            self.__vars["remove"] = True
        else:
            self.__vars["remove"] = False

    @property
    def converttype(self):
        """Give me decision to convert source file type."""
        return self.__vars["converttype"]

    @converttype.setter
    def converttype(self, arg):
        if isinstance(arg, bool):
            self.__vars["converttype"] = arg
        elif isinstance(arg, int) and arg == 1:
            self.__vars["converttype"] = True
        elif isinstance(arg, tk.IntVar) and arg.get() == 1:
            self.__vars["converttype"] = True
        else:
            self.__vars["converttype"] = False

    @property
    def srcdir(self):
        """Give me source directory with files to convert."""
        return self.__vars["srcdir"]

    @srcdir.setter
    def srcdir(self, arg):
        self.__vars["srcdir"] = arg

    @property
    def dstdir(self):
        """Give me destination directory for converted files."""
        return self.__vars["dstdir"]

    @dstdir.setter
    def dstdir(self, arg):
        self.__vars["dstdir"] = arg

    @property
    def suffix(self):
        """Suffix for pic filename."""
        return self.__vars["suffix"]

    @suffix.setter
    def suffix(self, arg):
        """Setter for suffix pic filename."""
        self.__vars["suffix"] = arg

    @property
    def templates(self):
        """Time templates."""
        return self.__templates

    def strtime(self, arg: str) -> str:
        """Timestamp from logs in local time convert to game time string.

        input: 2023-01-01T03:01:43Z
        output: 33090101-010143
        """
        # create struct_time
        str_time = time.strptime(arg, self.templates["logtime"])

        # create datetime object
        dt_obj = datetime(*str_time[:6])

        # convertion local time to game time
        dt_obj2 = dt_obj + self.__vars["timedelta"]

        return dt_obj2.strftime(self.templates["pictime"])

    def has_pillow(self):
        """Check if Pillow is present and importable."""
        self.logger.debug = "def has_pillow"

        # skip another test
        if self.__vars["pillow"]:
            return True

        for imod in [
            "PIL.Image",  # system PIL
            "picconv_libs.PIL311.Image",  # win [32|64] cpython 3.11
            "picconv_libs.PIL310.Image",  # win [32|64] cpython 3.10
            "picconv_libs.PIL310x.Image",  # debian [64] cpython 3.10
            "picconv_libs.PIL39.Image",  # win [32] cpython 3.9
            "picconv_libs.PIL3.Image",  # win [32|64] cpython 3.7
            "picconv_libs.PIL39x.Image",  # debian [64] cpython 3.9
        ]:
            try:
                image = importlib.import_module(imod)
                self.__vars["pillib"] = image
                self.__vars["pillow"] = True
                self.logger.debug = f"Found: {imod}"
                return True
            except Exception:
                continue

        self.logger.debug = "Not found"
        return False

    def convert(self, arg: dict) -> bool:
        """Pictures converter."""
        done = False
        convert = False

        localsuffix = os.path.splitext(arg["filename"])[1][1:]
        self.logger.debug = "def convert"
        self.logger.debug = f"Local suffix: {localsuffix}"
        self.logger.debug = f"Suffix: {self.__vars['suffix']}"
        self.logger.debug = f"Local pillow flag: {self.__vars['pillow']}"
        self.logger.debug = f"Local convert flag: {self.__vars['converttype']}"
        if self.__vars["pillow"] and self.__vars["converttype"]:
            localsuffix = self.__vars["suffix"]
            convert = True

        # check dirs
        if not Directory().is_directory(self.srcdir.dir):
            self.logger.error = f"Source directory is invalid: {self.srcdir.dir}"
            return done
        if not Directory().is_directory(self.dstdir.dir):
            self.logger.error = f"Destination directory is invalid: {self.dstdir.dir}"
            return done
        # check filename
        src = os.path.join(self.srcdir.dir, arg["filename"])
        if not os.path.exists(src):
            self.logger.error = f"Source file not found: {src}"
            return done
        # generate dst filename
        name = arg["body"]
        dst = os.path.join(
            self.dstdir.dir,
            self.templates["picfile"].format(
                self.strtime(arg["timestamp"]), name, localsuffix
            ),
        )
        # if dst file is present, generate new unique name
        count = 0
        while os.path.exists(dst):
            count += 1
            dst = os.path.join(
                self.dstdir.dir,
                self.templates["piccountfile"].format(
                    self.strtime(arg["timestamp"]), name, count, localsuffix
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
                self.logger.debug = f"try to remove file: {arg['filename']}....."
                os.remove(src)
                self.logger.debug = "... done"
        except Exception as ex:
            self.logger.error = f"ERROR: {ex.args[1]}"

        return done

    def __copy_file(self, src: str, dst: str) -> bool:
        """Copy file to new location."""
        # save file
        filename1 = os.path.basename(src)
        filename2 = os.path.basename(dst)
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
        filename1 = os.path.basename(src)
        filename2 = os.path.basename(dst)
        self.logger.debug = f"SRC: {src}"
        self.logger.debug = f"DST: {dst}"
        try:
            self.logger.debug = f"try to convert file: {filename1} to: {filename2}....."
            img = self.__vars["pillib"].open(src)
            img.save(dst)
            self.messages = f"{filename2} converted"
            self.logger.debug = "... done"
            return True
        except Exception as ex:
            self.logger.error = f"ERROR: {ex.args[1]}"
        return False
