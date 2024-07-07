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
from picconv_libs.edpc import EDPC
from picconv_libs.system import Directory, LogLevels


edpc_object = EDPC()


def plugin_start3(plugin_dir: str) -> str:
    """Load plugin into EDMC.

    plugin_dir:     plugin directory
    return:         local name of the plugin
    """
    edpc_object.logger.info = (
        f"Starting plugin {edpc_object.config_dialog.pluginname}..."
    )
    edpc_object.logger.debug = f"Plugin dir: {plugin_dir}"

    # set loglevel from config
    edpc_object.log_processor.loglevel = (
        LogLevels().get(config.get_str("loglevel"))
        if config.get_str("loglevel") is not None
        and LogLevels().has_key(config.get_str("loglevel"))
        else LogLevels().debug
    )  # type: ignore

    # config
    edpc_object.config_dialog.pic_src_dir = tk.StringVar(
        value=config.get_str("picsrcdir")
    )
    edpc_object.config_dialog.pic_dst_dir = tk.StringVar(
        value=config.get_str("picdstdir")
    )
    edpc_object.config_dialog.picmove = tk.IntVar(
        value=config.get_int(key="picmove", default=1)
    )
    edpc_object.config_dialog.pic_convert = tk.IntVar(
        value=config.get_int(key="picconvert", default=0)
    )
    edpc_object.config_dialog.pictype = tk.StringVar(
        value=config.get_str(key="pictype", default="jpg")
    )

    # init engine
    picsrcdir: Optional[tk.StringVar] = edpc_object.config_dialog.pic_src_dir
    if picsrcdir:
        edpc_object.engine.srcdir.dir = picsrcdir.get()
    picdstdir: Optional[tk.StringVar] = edpc_object.config_dialog.pic_dst_dir
    if picdstdir:
        edpc_object.engine.dstdir.dir = picdstdir.get()
    picmove: Optional[tk.IntVar] = edpc_object.config_dialog.picmove
    if picmove is not None:
        edpc_object.engine.remove = picmove.get()
    picconvert: Optional[tk.IntVar] = edpc_object.config_dialog.pic_convert
    if picconvert:
        edpc_object.engine.converttype = picconvert.get()
    pictype: Optional[tk.StringVar] = edpc_object.config_dialog.pictype
    if pictype:
        edpc_object.engine.suffix = pictype.get()

    # threading
    edpc_object.thworker.start()

    edpc_object.logger.info = "Done."
    return edpc_object.config_dialog.pluginname


def plugin_stop() -> None:
    """Stop plugin if EDMC is closing."""
    edpc_object.logger.info = (
        f"Stopping plugin {edpc_object.config_dialog.pluginname}..."
    )
    edpc_object.shutting_down = True
    edpc_object.qth.put(None)
    time.sleep(3)
    # edpc_object.thworker.join()
    edpc_object.logger.info = "Done."
    edpc_object.qlog.put(None)
    # edpc_object.thlog.join()


def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    """Return a TK Frame for adding to the EDMarketConnector settings dialog.

    parent:     Root Notebook object the preferences window uses
    cmdr:       The current commander
    is_beta:    If the game is currently a beta version
    """
    frame = edpc_object.config_dialog.create_dialog(parent)
    if not edpc_object.engine.has_pillow():
        edpc_object.logger.warning = "Picture type conversion not available."
        edpc_object.config_dialog.disable_conv_dialogs()
    return frame  # type: ignore


def plugin_app(parent: tk.Frame) -> Tuple[tk.Label, tk.Label]:
    """Create a pair of TK widgets for the EDMarketConnector main window.

    parent:     The root EDMarketConnector window
    """
    # By default widgets inherit the current theme's colors
    label = tk.Label(
        parent,
        text=f"{edpc_object.config_dialog.pluginname} v{edpc_object.config_dialog.version}:",
    )

    # Override theme's foreground color
    # edpc_object.cdial.status = tk.Label(parent, text="...", foreground="yellow")
    # or not
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
    picsrcdir: Optional[tk.StringVar] = edpc_object.config_dialog.pic_src_dir
    picdstdir: Optional[tk.StringVar] = edpc_object.config_dialog.pic_dst_dir
    picmove: Optional[tk.IntVar] = edpc_object.config_dialog.picmove
    picconvert: Optional[tk.IntVar] = edpc_object.config_dialog.pic_convert
    pictype: Optional[tk.StringVar] = edpc_object.config_dialog.pictype

    if Directory().is_directory(edpc_object.config_dialog.src_entry.get()):
        edpc_object.config_dialog.pic_src_dir = tk.StringVar(
            value=edpc_object.config_dialog.src_entry.get()
        )
    if picsrcdir:
        config.set("picsrcdir", picsrcdir.get())

    if Directory().is_directory(edpc_object.config_dialog.dst_entry.get()):
        edpc_object.config_dialog.pic_dst_dir = tk.StringVar(
            value=edpc_object.config_dialog.dst_entry.get()
        )
    if picdstdir:
        config.set("picdstdir", picdstdir.get())
    if picmove:
        config.set("picmove", picmove.get())
    if picconvert:
        config.set("picconvert", picconvert.get())
    if pictype:
        config.set("pictype", pictype.get())

    # engine update
    if picdstdir:
        edpc_object.engine.dstdir.dir = picdstdir.get()
    if picsrcdir:
        edpc_object.engine.srcdir.dir = picsrcdir.get()
    if picmove:
        edpc_object.engine.remove = picmove.get()
    if picconvert:
        edpc_object.engine.converttype = picconvert.get()
    if pictype:
        edpc_object.engine.suffix = pictype.get()
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
    if entry["event"] == "Screenshot":
        edpc_object.logger.info = "Got a new screenshot event."
        # edpc_object.logger.info = "cmdr: {}".format(cmdr)
        # edpc_object.logger.info = "is_beta: {}".format(is_beta)
        # edpc_object.logger.info = "system: {}".format(system)
        # edpc_object.logger.info = "station: {}".format(station)
        edpc_object.logger.debug = f"entry: {entry}"
        # edpc_object.logger.info = "state: {}".format(state)

        event: Dict[str, Any] = {}
        event["cmdr"] = cmdr
        event["timestamp"] = entry["timestamp"]
        event["filename"] = entry["Filename"][13:]
        event["width"] = entry["Width"]
        event["height"] = entry["Height"]
        if "System" in entry:
            event["system"] = entry["System"]
        if "Body" in entry:
            event["body"] = entry["Body"]
        else:
            system = ""
            if "System" in entry:
                system = f"{entry['System']} "
            event["body"] = f"{system}({station})"

        edpc_object.logger.info = "Put them in the queue..."
        edpc_object.qth.put(event)
        edpc_object.logger.info = "Done."
