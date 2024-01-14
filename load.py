# -*- coding: UTF-8 -*-
"""
Created on 18 dec 2022.

@author: szumak@virthost.pl
"""

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
    edpc_object.logger.info = f"Starting plugin {edpc_object.cdial.pluginname}..."
    edpc_object.logger.debug = f"Plugin dir: {plugin_dir}"

    # set loglevel from config
    edpc_object.log_processor.loglevel = (
        LogLevels().get(config.get_str("loglevel"))
        if config.get_str("loglevel") is not None
        and LogLevels().has_key(config.get_str("loglevel"))
        else LogLevels().debug
    ) # type: ignore

    # config
    edpc_object.cdial.picsrcdir = tk.StringVar(value=config.get_str("picsrcdir"))
    edpc_object.cdial.picdstdir = tk.StringVar(value=config.get_str("picdstdir"))
    edpc_object.cdial.picmove = tk.IntVar(
        value=config.get_int(key="picmove", default=1)
    )
    edpc_object.cdial.picconvert = tk.IntVar(
        value=config.get_int(key="picconvert", default=0)
    )
    edpc_object.cdial.pictype = tk.StringVar(
        value=config.get_str(key="pictype", default="jpg")
    )

    # init engine
    if edpc_object.cdial.picsrcdir is not None:
        edpc_object.engine.srcdir.dir = edpc_object.cdial.picsrcdir.get()
    if edpc_object.cdial.picdstdir is not None:
        edpc_object.engine.dstdir.dir = edpc_object.cdial.picdstdir.get()
    if edpc_object.cdial.picmove is not None:
        edpc_object.engine.remove = edpc_object.cdial.picmove.get()
    if edpc_object.cdial.picconvert is not None:
        edpc_object.engine.converttype = edpc_object.cdial.picconvert.get()
    if edpc_object.cdial.pictype is not None:
        edpc_object.engine.suffix = edpc_object.cdial.pictype.get()

    # threading
    edpc_object.thworker.start()

    edpc_object.logger.info = "Done."
    return edpc_object.cdial.pluginname


def plugin_stop() -> None:
    """Stop plugin if EDMC is closing."""
    edpc_object.logger.info = f"Stopping plugin {edpc_object.cdial.pluginname}..."
    edpc_object.shutting_down = True
    edpc_object.qth.put(None)
    edpc_object.thworker.join()
    edpc_object.logger.info = "Done."
    edpc_object.qlog.put(None)
    edpc_object.thlog.join()


def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    """Return a TK Frame for adding to the EDMarketConnector settings dialog.

    parent:     Root Notebook object the preferences window uses
    cmdr:       The current commander
    is_beta:    If the game is currently a beta version
    """
    frame = edpc_object.cdial.create_dialog(parent)
    if not edpc_object.engine.has_pillow():
        edpc_object.logger.warning = "Picture type conversion not available."
        edpc_object.cdial.disable_conv_dialogs()
    return frame  # type: ignore


def plugin_app(parent: tk.Frame) -> Tuple[tk.Label, tk.Label]:
    """Create a pair of TK widgets for the EDMarketConnector main window.

    parent:     The root EDMarketConnector window
    """
    # By default widgets inherit the current theme's colors
    label = tk.Label(
        parent, text=f"{edpc_object.cdial.pluginname} v{edpc_object.cdial.version}:"
    )

    # Override theme's foreground color
    # edpc_object.cdial.status = tk.Label(parent, text="...", foreground="yellow")
    # or not
    edpc_object.cdial.status = tk.Label(parent, text="")
    return label, edpc_object.cdial.status  # type: ignore


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    """Save settings.

    cmdr:       The current commander
    is_beta:    If the game is currently a beta version
    """
    edpc_object.logger.info = "config was changed"
    edpc_object.log_processor.loglevel = LogLevels().get(config.get_str("loglevel"))

    # save settings
    if Directory().is_directory(edpc_object.cdial.src_entry.get()):
        edpc_object.cdial.picsrcdir = tk.StringVar(
            value=edpc_object.cdial.src_entry.get()
        )
    config.set("picsrcdir", edpc_object.cdial.picsrcdir.get())

    if Directory().is_directory(edpc_object.cdial.dst_entry.get()):
        edpc_object.cdial.picdstdir = tk.StringVar(
            value=edpc_object.cdial.dst_entry.get()
        )
    config.set("picdstdir", edpc_object.cdial.picdstdir.get())
    config.set("picmove", edpc_object.cdial.picmove.get())
    config.set("picconvert", edpc_object.cdial.picconvert.get())
    config.set("pictype", edpc_object.cdial.pictype.get())

    # engine update
    edpc_object.engine.dstdir.dir = edpc_object.cdial.picdstdir.get()
    edpc_object.engine.srcdir.dir = edpc_object.cdial.picsrcdir.get()
    edpc_object.engine.remove = edpc_object.cdial.picmove.get()
    edpc_object.engine.converttype = edpc_object.cdial.picconvert.get()
    edpc_object.engine.suffix = edpc_object.cdial.pictype.get()
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
