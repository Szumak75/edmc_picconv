# -*- coding: UTF-8 -*-
"""
Created on 02 jan 2023.

@author: szumak@virthost.pl
"""

from inspect import currentframe
import tkinter as tk
from queue import Queue, SimpleQueue
from tkinter import filedialog, ttk
from typing import Optional, Dict, Union, Any

import myNotebook as nb
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from picconv_libs.base_log import BLogClient
from picconv_libs.system import Env, LogClient


class ConfigDialog(BLogClient, NoDynamicAttributes):
    """Create config dialog for plugin."""

    __vars: Dict[str, Any] = None  # type: ignore
    __pic_status: nb.Label = None  # type: ignore

    def __init__(self, queue: Union[Queue, SimpleQueue]) -> None:
        """Initialize ConfigDialog class."""
        self.__vars = {
            "pluginname": None,
            "version": None,
            "src_entry": None,
            "dst_entry": None,
            "picmove_check": None,
            "picconv_check": None,
            "pictype_check": None,
        }
        self.__vars["picsrcdir"] = None  #: Optional[tk.StringVar]
        self.__vars["picdstdir"] = None  #: Optional[tk.StringVar]
        self.__vars["pictype"] = tk.StringVar(value="jpg")
        self.__vars["picconvert"] = tk.IntVar(value=0)
        self.__vars["picmove"] = tk.IntVar(value=1)
        self.__vars["status"] = None  #: Optional[tk.Label]

        # init log subsystem
        if not isinstance(queue, (Queue, SimpleQueue)):
            raise Raise.error(
                f"Queue or SimpleQueue type expected, '{type(queue)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self.logger = LogClient(queue)

    def create_dialog(self, parent: nb.Notebook) -> nb.Frame:
        """Create and return config dialog."""
        frame = nb.Frame(parent)

        # grid config
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=5)
        frame.columnconfigure(2, weight=1)

        # src dir row
        rc_src = 0
        frame.rowconfigure(rc_src, weight=1)
        frame.rowconfigure(rc_src + 1, weight=1)
        # dst dir row
        rc_dst = rc_src + 2
        frame.rowconfigure(rc_dst, weight=1)
        frame.rowconfigure(rc_dst + 1, weight=1)
        # move file
        rc_mf = rc_dst + 2
        frame.rowconfigure(rc_mf, weight=1)
        # Separator
        rc_sep = rc_mf + 1
        frame.rowconfigure(rc_sep, weight=1)
        # pic converter
        rc_conv = rc_sep + 1
        frame.rowconfigure(rc_conv, weight=1)
        frame.rowconfigure(rc_conv + 1, weight=1)
        frame.rowconfigure(rc_conv + 2, weight=1)
        frame.rowconfigure(rc_conv + 3, weight=1)

        # spring row
        rc_spr = rc_conv + 4
        frame.rowconfigure(rc_spr, weight=100)

        # stat row
        rc_stat = rc_spr + 1
        frame.rowconfigure(rc_stat, weight=1)

        # dialogs config
        # src dir
        nb.Label(frame, text="ED Screenshot Directory:").grid(
            padx=10, row=rc_src, column=0, columnspan=3, sticky=tk.W
        )
        self.src_entry = nb.Entry(frame, textvariable=self.picsrcdir)
        self.src_entry.grid(
            padx=10, row=rc_src + 1, column=0, columnspan=2, sticky=tk.EW
        )
        nb.Button(frame, text="Choose Directory", command=self.button_src_dir).grid(
            padx=10, row=rc_src + 1, column=2, sticky=tk.E
        )

        # dst dir
        nb.Label(frame, text="Screenshot Output Directory:").grid(
            padx=10, row=rc_dst, column=0, columnspan=3, sticky=tk.W
        )
        self.dst_entry = nb.Entry(frame, textvariable=self.picdstdir)
        self.dst_entry.grid(
            padx=10, row=rc_dst + 1, column=0, columnspan=2, sticky=tk.EW
        )
        nb.Button(frame, text="Choose Directory", command=self.button_dst_dir).grid(
            padx=10, row=rc_dst + 1, column=2, sticky=tk.E
        )

        # move file
        self.picmove_check = nb.Checkbutton(
            frame,
            text="delete source file",
            variable=self.picmove,
            onvalue=1,
            offvalue=0,
        )
        self.picmove_check.grid(padx=10, row=rc_mf, column=0, columnspan=2, sticky=tk.W)

        # separator
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            padx=10, row=rc_sep, pady=8, column=0, columnspan=2, sticky=tk.EW
        )

        # pic conv
        self.picconv_check = nb.Checkbutton(
            frame,
            text="enable type convert",
            variable=self.picconvert,
            onvalue=1,
            offvalue=0,
        )
        self.picconv_check.grid(
            padx=10, row=rc_conv, column=0, columnspan=2, sticky=tk.W
        )
        nb.Radiobutton(
            frame, text="JPG", value="jpg", variable=self.__vars["pictype"]
        ).grid(padx=10, row=rc_conv + 1, column=1, sticky=tk.W)
        nb.Radiobutton(
            frame, text="PNG", value="png", variable=self.__vars["pictype"]
        ).grid(padx=10, row=rc_conv + 2, column=1, sticky=tk.W)
        nb.Radiobutton(
            frame, text="TIFF", value="tif", variable=self.__vars["pictype"]
        ).grid(padx=10, row=rc_conv + 3, column=1, sticky=tk.W)

        # status
        self.__pic_status = nb.Label(frame, text="")
        self.pic_status.grid(padx=10, row=rc_stat, column=0, columnspan=3, sticky=tk.W)

        return frame

    def disable_conv_dialogs(self) -> None:
        """Disable unused entry."""
        # entry.config(state="disabled")
        self.picconv_check.config(state="disabled")
        self.pic_status["text"] = (
            "Type conversion unavailable due to missing libraries."
        )

    def button_src_dir(self) -> None:
        """Run Button callback."""
        self.logger.info = "Src dir button pressed"
        tool = Env()
        out = filedialog.askdirectory(initialdir=tool.check_dir(self.src_entry.get()))
        if isinstance(out, str) and len(out) > 0:
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, out)
            # check if directory exists
            tmp = tool.check_dir(out)
            if out != tmp:
                self.pic_status["text"] = "WARNING: check source directory"
            else:
                self.pic_status["text"] = ""
        else:
            entry: str = self.src_entry.get()
            tmp: str = tool.check_dir(entry)
            if entry != tmp:
                self.pic_status["text"] = "WARNING: source directory not found"
                self.src_entry.delete(0, tk.END)
            else:
                self.pic_status["text"] = ""
        self.logger.info = out

    def button_dst_dir(self) -> None:
        """Run Button callback."""
        self.logger.info = "Dst dir button pressed"
        tool = Env()
        out = filedialog.askdirectory(initialdir=tool.check_dir(self.dst_entry.get()))
        if isinstance(out, str) and len(out) > 0:
            self.dst_entry.delete(0, tk.END)
            self.dst_entry.insert(0, out)
            # check if directory exists
            tmp = tool.check_dir(out)
            self.logger.info = f"Out: {out}"
            self.logger.info = f"Check: {tmp}"
            if out != tmp:
                self.pic_status["text"] = "WARNING: check destination directory"
            else:
                self.pic_status["text"] = ""
        else:
            entry: str = self.dst_entry.get()
            tmp: str = tool.check_dir(entry)
            self.logger.info = f"Entry: {entry}"
            self.logger.info = f"Check: {tmp}"
            if entry != tmp:
                self.pic_status["text"] = "WARNING: destination directory not found"
                self.dst_entry.delete(0, tk.END)
            else:
                (self.pic_status)["text"] = ""
        self.logger.info = out

    @property
    def pluginname(self) -> str:
        """Give me the name of plugin."""
        return self.__vars["pluginname"]

    @pluginname.setter
    def pluginname(self, arg: str) -> None:
        self.__vars["pluginname"] = arg

    @property
    def version(self) -> str:
        """Give me the version of plugin."""
        return self.__vars["version"]

    @version.setter
    def version(self, arg: str) -> None:
        self.__vars["version"] = arg

    @property
    def status(self) -> Optional[tk.Label]:
        """Give me the version of plugin."""
        return self.__vars["status"]

    @status.setter
    def status(self, arg: tk.Label) -> None:
        self.__vars["status"] = arg

    @property
    def src_entry(self) -> nb.Entry:
        """Give me the Entry with source directory."""
        return self.__vars["src_entry"]

    @src_entry.setter
    def src_entry(self, arg: nb.Entry) -> None:
        self.__vars["src_entry"] = arg

    @property
    def dst_entry(self) -> nb.Entry:
        """Give me the Entry with destination directory."""
        return self.__vars["dst_entry"]

    @dst_entry.setter
    def dst_entry(self, arg: nb.Entry) -> None:
        self.__vars["dst_entry"] = arg

    @property
    def pic_status(self) -> nb.Label:
        """Give me access to the pic_status Label."""
        # return self.__vars['pic_status']
        return self.__pic_status

    @pic_status.setter
    def pic_status(self, arg: nb.Label) -> None:
        # self.__vars["pic_status"] = arg
        self.__pic_status = arg

    @property
    def picsrcdir(self) -> Optional[tk.StringVar]:
        """Give me string dir."""
        return self.__vars["picsrcdir"]

    @picsrcdir.setter
    def picsrcdir(self, arg: tk.StringVar) -> None:
        self.__vars["picsrcdir"] = arg

    @property
    def picdstdir(self) -> Optional[tk.StringVar]:
        """Give me string dir."""
        return self.__vars["picdstdir"]

    @picdstdir.setter
    def picdstdir(self, arg: tk.StringVar) -> None:
        self.__vars["picdstdir"] = arg

    @property
    def picmove_check(self) -> nb.Checkbutton:
        """Give me access to the picmove Check Button."""
        return self.__vars["picmove_check"]

    @picmove_check.setter
    def picmove_check(self, arg: nb.Checkbutton) -> None:
        self.__vars["picmove_check"] = arg

    @property
    def picconv_check(self) -> nb.Checkbutton:
        """Give me access to the picconv Check Button."""
        return self.__vars["picconv_check"]

    @picconv_check.setter
    def picconv_check(self, arg: nb.Checkbutton) -> None:
        self.__vars["picconv_check"] = arg

    @property
    def picmove(self) -> Optional[tk.IntVar]:
        """Give me picmove value Int."""
        return self.__vars["picmove"]

    @picmove.setter
    def picmove(self, arg: tk.IntVar) -> None:
        self.__vars["picmove"] = arg

    @property
    def picconvert(self) -> Optional[tk.IntVar]:
        """Give me picconvert value Int."""
        return self.__vars["picconvert"]

    @picconvert.setter
    def picconvert(self, arg: tk.IntVar) -> None:
        self.__vars["picconvert"] = arg

    @property
    def pictype(self) -> Optional[tk.StringVar]:
        """Give me pictype value Str."""
        return self.__vars["pictype"]

    @pictype.setter
    def pictype(self, arg: tk.StringVar) -> None:
        self.__vars["pictype"] = arg
