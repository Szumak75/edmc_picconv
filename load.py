# -*- coding: UTF-8 -*-
"""
Created on 18 dec 2022.

@author: szumak@virthost.pl
"""

import time
import tkinter as tk
from typing import Any, Dict, Optional, Tuple


import myNotebook as nb
from config import config
from edpc.edpc import EDPC
from edpc.jsktoolbox.edmctool.system import Directory
from edpc.jsktoolbox.edmctool.logs import LogLevels

from edpc.keys import EDPCKeys

edpc_object = EDPC()


def plugin_start3(plugin_dir: str) -> str:
    """Load plugin into EDMC.

    plugin_dir:     plugin directory
    return:         local name of the plugin
    """
    edpc_object.logger.info = (
        f"Starting plugin {edpc_object.config_dialog.plugin_name}..."
    )
    edpc_object.logger.debug = f"Plugin dir: {plugin_dir}"

    # set loglevel from config
    edpc_object.log_processor.loglevel = (
        LogLevels().get(config.get_str(EDPCKeys.CONF_LOG_LEVEL))
        if config.get_str(EDPCKeys.CONF_LOG_LEVEL) is not None
        and LogLevels().has_key(config.get_str(EDPCKeys.CONF_LOG_LEVEL))
        else LogLevels().debug
    )  # type: ignore

    # config
    edpc_object.config_dialog.pic_src_dir = tk.StringVar(
        value=config.get_str(EDPCKeys.CONF_PIC_SRC_DIR)
    )
    edpc_object.config_dialog.pic_dst_dir = tk.StringVar(
        value=config.get_str(EDPCKeys.CONF_PIC_DST_DIR)
    )
    edpc_object.config_dialog.pic_move = tk.IntVar(
        value=config.get_int(key=EDPCKeys.CONF_PIC_MOVE, default=1)
    )
    edpc_object.config_dialog.pic_convert = tk.IntVar(
        value=config.get_int(key=EDPCKeys.CONF_PIC_CONVERT, default=0)
    )
    edpc_object.config_dialog.pic_type = tk.StringVar(
        value=config.get_str(key=EDPCKeys.CONF_PIC_TYPE, default="jpg")
    )

    # init engine
    pic_src_dir: Optional[tk.StringVar] = edpc_object.config_dialog.pic_src_dir
    if pic_src_dir:
        edpc_object.engine.src_dir.dir = pic_src_dir.get()
    pic_dst_dir: Optional[tk.StringVar] = edpc_object.config_dialog.pic_dst_dir
    if pic_dst_dir:
        edpc_object.engine.dst_dir.dir = pic_dst_dir.get()
    pic_move: Optional[tk.IntVar] = edpc_object.config_dialog.pic_move
    if pic_move is not None:
        edpc_object.engine.remove = pic_move.get()
    pic_convert: Optional[tk.IntVar] = edpc_object.config_dialog.pic_convert
    if pic_convert:
        edpc_object.engine.convert_type = pic_convert.get()
    pic_type: Optional[tk.StringVar] = edpc_object.config_dialog.pic_type
    if pic_type:
        edpc_object.engine.suffix = pic_type.get()

    # threading
    edpc_object.th_worker_engine.start()

    edpc_object.logger.info = "Done."
    return edpc_object.config_dialog.plugin_name


def plugin_stop() -> None:
    """Stop plugin if EDMC is closing."""
    edpc_object.logger.info = (
        f"Stopping plugin {edpc_object.config_dialog.plugin_name}..."
    )
    edpc_object.shutting_down = True
    edpc_object.qth.put(None)
    time.sleep(3)
    edpc_object.logger.info = "Done."
    edpc_object.qlog.put(None)


def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    """Return a TK Frame for adding to the EDMarketConnector settings dialog.

    parent:     Root Notebook object the preferences window uses
    cmdr:       The current commander
    is_beta:    If the game is currently a beta version
    """
    frame = edpc_object.config_dialog.create_dialog(parent)
    return frame  # type: ignore


def plugin_app(parent: tk.Frame) -> Tuple[tk.Label, tk.Label]:
    """Create a pair of TK widgets for the EDMarketConnector main window.

    parent:     The root EDMarketConnector window
    """
    # By default widgets inherit the current theme's colors
    label = tk.Label(
        parent,
        text=f"{edpc_object.config_dialog.plugin_name}:",
    )

    edpc_object.config_dialog.status = tk.Label(parent, text="")
    return label, edpc_object.config_dialog.status  # type: ignore


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    """Save settings.

    cmdr:       The current commander
    is_beta:    If the game is currently a beta version
    """
    edpc_object.logger.info = "config was changed"
    loglevel = LogLevels().get(config.get_str("loglevel"))
    if loglevel is not None:
        edpc_object.log_processor.loglevel = loglevel

    # save settings
    pic_src_dir: Optional[tk.StringVar] = edpc_object.config_dialog.pic_src_dir
    pic_dst_dir: Optional[tk.StringVar] = edpc_object.config_dialog.pic_dst_dir
    pic_move: Optional[tk.IntVar] = edpc_object.config_dialog.pic_move
    pic_convert: Optional[tk.IntVar] = edpc_object.config_dialog.pic_convert
    pic_type: Optional[tk.StringVar] = edpc_object.config_dialog.pic_type

    if Directory().is_directory(edpc_object.config_dialog.src_entry.get()):
        edpc_object.config_dialog.pic_src_dir = tk.StringVar(
            value=edpc_object.config_dialog.src_entry.get()
        )
    if pic_src_dir:
        config.set(EDPCKeys.CONF_PIC_SRC_DIR, pic_src_dir.get())

    if Directory().is_directory(edpc_object.config_dialog.dst_entry.get()):
        edpc_object.config_dialog.pic_dst_dir = tk.StringVar(
            value=edpc_object.config_dialog.dst_entry.get()
        )
    if pic_dst_dir:
        config.set(EDPCKeys.CONF_PIC_DST_DIR, pic_dst_dir.get())
    if pic_move:
        config.set(EDPCKeys.CONF_PIC_MOVE, pic_move.get())
    if pic_convert:
        config.set(EDPCKeys.CONF_PIC_CONVERT, pic_convert.get())
    if pic_type:
        config.set(EDPCKeys.CONF_PIC_TYPE, pic_type.get())

    # engine update
    if pic_dst_dir:
        edpc_object.engine.dst_dir.dir = pic_dst_dir.get()
    if pic_src_dir:
        edpc_object.engine.src_dir.dir = pic_src_dir.get()
    if pic_move:
        edpc_object.engine.remove = pic_move.get()
    if pic_convert:
        edpc_object.engine.convert_type = pic_convert.get()
    if pic_type:
        edpc_object.engine.suffix = pic_type.get()
    edpc_object.logger.info = "update complete"


def journal_entry(
    cmdr: str,
    is_beta: bool,
    system: str,
    station: str,
    entry: Dict[str, Any],
    state: Dict[str, Any],
) -> Optional[str]:
    """Get new entry in the game's journal.

    cmdr:       Current commander name
    is_beta:    Is the game currently in beta
    system:     Current system, if known
    station:    Current station, if any
    entry:      The journal event
    state:      More info about the commander, their ship, and their cargo
    """
    if entry[EDPCKeys.P_EVENT] == EDPCKeys.P_SCREENSHOT:
        edpc_object.logger.info = "Got a new screenshot event."
        edpc_object.logger.debug = f"entry: {entry}"

        event: Dict[str, Any] = {}
        event[EDPCKeys.P_CMDR] = cmdr
        event[EDPCKeys.P_TIMESTAMP] = entry[EDPCKeys.P_TIMESTAMP]
        event[EDPCKeys.P_FILENAME] = entry[EDPCKeys.P_FILENAME][13:]
        event[EDPCKeys.P_WIDTH] = entry[EDPCKeys.P_WIDTH]
        event[EDPCKeys.P_HEIGHT] = entry[EDPCKeys.P_HEIGHT]
        if EDPCKeys.P_SYSTEM in entry:
            event[EDPCKeys.P_SYSTEM] = entry[EDPCKeys.P_SYSTEM]
        if EDPCKeys.P_BODY in entry:
            event[EDPCKeys.P_BODY] = entry[EDPCKeys.P_BODY]
        else:
            system = ""
            if EDPCKeys.P_SYSTEM in entry:
                system = f"{entry[EDPCKeys.P_SYSTEM]} "
            event[EDPCKeys.P_BODY] = f"{system}({station})"

        edpc_object.logger.info = "Put them in the queue..."
        edpc_object.qth.put(event)
        edpc_object.logger.info = "Done."
