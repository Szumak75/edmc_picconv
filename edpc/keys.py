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

    # PARSER
    P_TIMESTAMP: str = "timestamp"
    P_FILENAME: str = "Filename"
    P_WIDTH: str = "Width"
    P_HEIGHT: str = "Height"
    P_SYSTEM: str = "System"
    P_BODY: str = "Body"
    P_CMDR: str = "Cmdr"
    P_EVENT: str = "event"
    P_SCREENSHOT: str = "Screenshot"

    # CONFIG
    CONF_PIC_SRC_DIR: str = "picsrcdir"
    CONF_PIC_DST_DIR: str = "picdstdir"
    CONF_PIC_MOVE: str = "picmove"
    CONF_PIC_CONVERT: str = "picconvert"
    CONF_PIC_TYPE: str = "pictype"
    CONF_LOG_LEVEL: str = "loglevel"

    # SYSTEM
    CONFIG_DIALOG: str = "__config_dialog__"
    DIR: str = "__dir__"
    ENGINE: str = "__engine__"
    LOGGER: str = "__logger__"
    LOG_PROCESSOR: str = "__log_processor__"
    MESSAGES: str = "__messages__"
    QLOG: str = "__qlog__"
    SHUTTING_DOWN: str = "__shutting_down__"
    TH_LOG: str = "__th_log__"
    TH_QUEUE: str = "__th_queue__"
    TH_WORKER: str = "__th_worker__"

    # converter
    CONVERT_TYPE: str = "__convert_type__"
    DELTA_TIME: str = "__time_delta__"
    DST_DIR: str = "__dst_dir__"
    REMOVE: str = "__remove__"
    SRC_DIR: str = "__src_dir__"
    SUFFIX: str = "__suffix__"

    # template
    LOG_TIME: str = "__log_time__"
    PIC_COUNT_FILE: str = "__pic_count_file__"
    PIC_FILE: str = "__pic_file__"
    PIC_TIME: str = "__pic_time__"

    # DIALOG
    DST_ENTRY: str = "__dst_entry__"
    PIC_CONVERT: str = "__pic_convert__"
    PIC_CONV_CHECK: str = "__pic_conv_check__"
    PIC_DST_DIR: str = "__pic_dst_dir__"
    PIC_MOVE: str = "__pic_move__"
    PIC_MOVE_CHECK: str = "__pic_move_check__"
    PIC_SRC_DIR: str = "__pic_src_dir__"
    PIC_STATUS: str = "__pic_status__"
    PIC_TYPE: str = "__pic_type__"
    PIC_TYPE_CHECK: str = "__pic_type_check__"
    PLUGIN_NAME: str = "__plugin_name__"
    SRC_ENTRY: str = "__src_entry__"
    STATUS: str = "__status__"
    PLUGIN_VERSION: str = "__version__"


# #[EOF]#######################################################################
