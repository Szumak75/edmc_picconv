# -*- coding: UTF-8 -*-
"""
Created on 02 jan 2023.

@author: szumak@virthost.pl
"""

from inspect import currentframe
import tkinter as tk
from queue import Queue, SimpleQueue
from tkinter import filedialog, ttk
from typing import Optional, Union

import myNotebook as nb
from edpc.jsktoolbox.raisetool import Raise
from edpc.jsktoolbox.edmctool.base import BLogClient
from edpc.jsktoolbox.edmctool.system import EnvLocal
from edpc.jsktoolbox.edmctool.logs import LogClient
from edpc.keys import EDPCKeys


class ConfigDialog(BLogClient):
    """Create config dialog for plugin."""

    def __init__(self, queue: Union[Queue, SimpleQueue]) -> None:
        """Initialize ConfigDialog class."""
        self._set_data(
            key=EDPCKeys.PLUGIN_NAME, value=None, set_default_type=Optional[str]
        )
        self._set_data(
            key=EDPCKeys.PLUGIN_VERSION, value=None, set_default_type=Optional[str]
        )
        self._set_data(
            key=EDPCKeys.SRC_ENTRY, value=None, set_default_type=Optional[nb.EntryMenu]
        )
        self._set_data(
            key=EDPCKeys.DST_ENTRY, value=None, set_default_type=Optional[nb.EntryMenu]
        )
        self._set_data(
            key=EDPCKeys.PIC_MOVE_CHECK,
            value=None,
            set_default_type=Optional[nb.Checkbutton],
        )
        self._set_data(
            key=EDPCKeys.PIC_CONV_CHECK,
            value=None,
            set_default_type=Optional[nb.Checkbutton],
        )
        self._set_data(
            key=EDPCKeys.PIC_TYPE_CHECK,
            value=None,
            set_default_type=Optional[nb.Checkbutton],
        )
        self._set_data(
            key=EDPCKeys.PIC_SRC_DIR,
            value=None,
            set_default_type=Optional[tk.StringVar],
        )
        self._set_data(
            key=EDPCKeys.PIC_DST_DIR,
            value=None,
            set_default_type=Optional[tk.StringVar],
        )
        self._set_data(
            key=EDPCKeys.PIC_TYPE,
            value=tk.StringVar(value="jpg"),
            set_default_type=tk.StringVar,
        )
        self._set_data(
            key=EDPCKeys.PIC_CONVERT,
            value=tk.IntVar(value=0),
            set_default_type=tk.IntVar,
        )
        self._set_data(
            key=EDPCKeys.PIC_MOVE,
            value=tk.IntVar(value=1),
            set_default_type=tk.IntVar,
        )
        self._set_data(
            key=EDPCKeys.STATUS, value=None, set_default_type=Optional[tk.Label]
        )
        self._set_data(
            key=EDPCKeys.PIC_STATUS, value=None, set_default_type=Optional[nb.Label]
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
    def plugin_name(self) -> str:
        """Give me the name of plugin."""
        return self._get_data(key=EDPCKeys.PLUGIN_NAME)  # type: ignore

    @plugin_name.setter
    def plugin_name(self, arg: str) -> None:
        self._set_data(key=EDPCKeys.PLUGIN_NAME, value=arg)

    @property
    def version(self) -> str:
        """Give me the version of plugin."""
        return self._get_data(key=EDPCKeys.PLUGIN_VERSION)  # type: ignore

    @version.setter
    def version(self, arg: str) -> None:
        self._set_data(key=EDPCKeys.PLUGIN_VERSION, value=arg)

    @property
    def status(self) -> Optional[tk.Label]:
        """Give me the version of plugin."""
        return self._get_data(key=EDPCKeys.STATUS)

    @status.setter
    def status(self, arg: tk.Label) -> None:
        self._set_data(key=EDPCKeys.STATUS, value=arg)

    @property
    def src_entry(self) -> nb.EntryMenu:
        """Give me the Entry with source directory."""
        return self._get_data(key=EDPCKeys.SRC_ENTRY)  # type: ignore

    @src_entry.setter
    def src_entry(self, arg: nb.EntryMenu) -> None:
        self._set_data(key=EDPCKeys.SRC_ENTRY, value=arg)

    @property
    def dst_entry(self) -> nb.EntryMenu:
        """Give me the Entry with destination directory."""
        return self._get_data(key=EDPCKeys.DST_ENTRY)  # type: ignore

    @dst_entry.setter
    def dst_entry(self, arg: nb.EntryMenu) -> None:
        self._set_data(key=EDPCKeys.DST_ENTRY, value=arg)

    @property
    def pic_status(self) -> nb.Label:
        """Give me access to the pic_status Label."""
        # return self.__vars['pic_status']
        return self._get_data(key=EDPCKeys.PIC_STATUS)  # type: ignore

    @pic_status.setter
    def pic_status(self, arg: nb.Label) -> None:
        # self.__vars["pic_status"] = arg
        self._set_data(key=EDPCKeys.PIC_STATUS, value=arg)

    @property
    def pic_src_dir(self) -> Optional[tk.StringVar]:
        """Give me string dir."""
        return self._get_data(key=EDPCKeys.PIC_SRC_DIR)

    @pic_src_dir.setter
    def pic_src_dir(self, arg: tk.StringVar) -> None:
        self._set_data(key=EDPCKeys.PIC_SRC_DIR, value=arg)

    @property
    def pic_dst_dir(self) -> Optional[tk.StringVar]:
        """Give me string dir."""
        return self._get_data(key=EDPCKeys.PIC_DST_DIR)

    @pic_dst_dir.setter
    def pic_dst_dir(self, arg: tk.StringVar) -> None:
        self._set_data(key=EDPCKeys.PIC_DST_DIR, value=arg)

    @property
    def pic_move_check(self) -> nb.Checkbutton:
        """Give me access to the picmove Check Button."""
        return self._get_data(key=EDPCKeys.PIC_MOVE_CHECK)  # type: ignore

    @pic_move_check.setter
    def pic_move_check(self, arg: nb.Checkbutton) -> None:
        self._set_data(key=EDPCKeys.PIC_MOVE_CHECK, value=arg)

    @property
    def pic_conv_check(self) -> nb.Checkbutton:
        """Give me access to the picconv Check Button."""
        return self._get_data(key=EDPCKeys.PIC_CONV_CHECK)  # type: ignore

    @pic_conv_check.setter
    def pic_conv_check(self, arg: nb.Checkbutton) -> None:
        self._set_data(key=EDPCKeys.PIC_CONV_CHECK, value=arg)

    @property
    def pic_move(self) -> Optional[tk.IntVar]:
        """Give me picmove value Int."""
        return self._get_data(key=EDPCKeys.PIC_MOVE)

    @pic_move.setter
    def pic_move(self, arg: tk.IntVar) -> None:
        self._set_data(key=EDPCKeys.PIC_MOVE, value=arg)

    @property
    def pic_convert(self) -> Optional[tk.IntVar]:
        """Give me picconvert value Int."""
        return self._get_data(key=EDPCKeys.PIC_CONVERT)

    @pic_convert.setter
    def pic_convert(self, arg: tk.IntVar) -> None:
        self._set_data(key=EDPCKeys.PIC_CONVERT, value=arg)

    @property
    def pic_type(self) -> Optional[tk.StringVar]:
        """Give me pictype value Str."""
        return self._get_data(key=EDPCKeys.PIC_TYPE)

    @pic_type.setter
    def pic_type(self, arg: tk.StringVar) -> None:
        self._set_data(key=EDPCKeys.PIC_TYPE, value=arg)

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
        self.src_entry = nb.EntryMenu(frame, textvariable=self.pic_src_dir)
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
        self.dst_entry = nb.EntryMenu(frame, textvariable=self.pic_dst_dir)
        self.dst_entry.grid(
            padx=10, row=rc_dst + 1, column=0, columnspan=2, sticky=tk.EW
        )
        nb.Button(frame, text="Choose Directory", command=self.button_dst_dir).grid(
            padx=10, row=rc_dst + 1, column=2, sticky=tk.E
        )

        # move file
        self.pic_move_check = nb.Checkbutton(
            frame,
            text="delete source file",
            variable=self.pic_move,
            onvalue=1,
            offvalue=0,
        )
        self.pic_move_check.grid(
            padx=10, row=rc_mf, column=0, columnspan=2, sticky=tk.W
        )

        # separator
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            padx=10, row=rc_sep, pady=8, column=0, columnspan=2, sticky=tk.EW
        )

        # pic conv
        self.pic_conv_check = nb.Checkbutton(
            frame,
            text="enable type convert",
            variable=self.pic_convert,
            onvalue=1,
            offvalue=0,
        )
        self.pic_conv_check.grid(
            padx=10, row=rc_conv, column=0, columnspan=2, sticky=tk.W
        )
        nb.Radiobutton(
            frame,
            text="JPG",
            value="jpg",
            variable=self._get_data(key=EDPCKeys.PIC_TYPE),
        ).grid(padx=10, row=rc_conv + 1, column=1, sticky=tk.W)
        nb.Radiobutton(
            frame,
            text="PNG",
            value="png",
            variable=self._get_data(key=EDPCKeys.PIC_TYPE),
        ).grid(padx=10, row=rc_conv + 2, column=1, sticky=tk.W)
        nb.Radiobutton(
            frame,
            text="TIFF",
            value="tif",
            variable=self._get_data(key=EDPCKeys.PIC_TYPE),
        ).grid(padx=10, row=rc_conv + 3, column=1, sticky=tk.W)

        # status
        self._set_data(key=EDPCKeys.PIC_STATUS, value=nb.Label(frame, text=""))
        self.pic_status.grid(padx=10, row=rc_stat, column=0, columnspan=3, sticky=tk.W)

        return frame

    def button_src_dir(self) -> None:
        """Run Button callback."""
        self.logger.info = "Src dir button pressed"
        tool = EnvLocal()
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
        tool = EnvLocal()
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
