# -*- coding: UTF-8 -*-
"""
  edpc.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 14.01.2024, 18:01:41
  
  Purpose: EDPC main class.
"""


from edpc.base_log import BLogClient, BLogProcessor
from edpc.converter import PicConverter
from edpc.dialogs import ConfigDialog
from edpc.system import LogClient, LogProcessor


from edpc.jsktoolbox.datetool import Timestamp
from edpc.keys import EDPCKeys

import time
from queue import Queue, SimpleQueue, Empty
from threading import Thread
from typing import List, Union


class EDPC(BLogProcessor, BLogClient):
    """EDPC main class."""

    def __init__(self) -> None:
        """Initialize main class."""
        self.shutting_down = False

        self.plugin_name = "EDPC"
        version = "0.4.0"

        # logging subsystem
        self.qlog = SimpleQueue()
        self.log_processor = LogProcessor(self.plugin_name)
        self.logger = LogClient(self.qlog)

        # logging thread
        self.th_log = Thread(
            target=self._th_logger, name=f"{self.plugin_name} log worker", daemon=True
        )
        self.th_log.start()

        # config dialog
        self.config_dialog = ConfigDialog(self.qlog)
        self.config_dialog.plugin_name = self.plugin_name
        self.config_dialog.version = version

        # worker thread
        self.th_worker_engine = Thread(
            target=self._th_worker,
            name=f"{self.config_dialog.plugin_name} worker",
            daemon=True,
        )

        self._set_data(
            key=EDPCKeys.TH_QUEUE,
            value=SimpleQueue(),
            set_default_type=Union[Queue, SimpleQueue],
        )
        self.engine = PicConverter(self.qlog)

    @property
    def engine(self) -> PicConverter:
        """Get PicConverter instance."""
        return self._get_data(
            key=EDPCKeys.ENGINE,
        )  # type: ignore

    @engine.setter
    def engine(self, value: PicConverter) -> None:
        """Set PicConverter instance."""
        self._set_data(key=EDPCKeys.ENGINE, value=value, set_default_type=PicConverter)

    @property
    def config_dialog(self) -> ConfigDialog:
        return self._get_data(key=EDPCKeys.CONFIG_DIALOG)  # type: ignore

    @config_dialog.setter
    def config_dialog(self, value: ConfigDialog) -> None:
        self._set_data(
            key=EDPCKeys.CONFIG_DIALOG, value=value, set_default_type=ConfigDialog
        )

    @property
    def th_worker_engine(self) -> Thread:
        """Give me access to thworker variable."""
        return self._get_data(key=EDPCKeys.TH_WORKER)  # type: ignore

    @th_worker_engine.setter
    def th_worker_engine(self, value: Thread) -> None:
        self._set_data(
            key=EDPCKeys.TH_WORKER,
            value=value,
            set_default_type=Thread,
        )

    @property
    def plugin_name(self) -> str:
        """Give me access to pluginname variable."""
        return self._get_data(
            key=EDPCKeys.PLUGIN_NAME, default_value=""
        )  # type: ignore

    @plugin_name.setter
    def plugin_name(self, value: str) -> None:
        self._set_data(key=EDPCKeys.PLUGIN_NAME, value=value, set_default_type=str)

    @property
    def shutting_down(self) -> bool:
        """Give me access to shutting_down flag."""
        return self._get_data(key=EDPCKeys.SHUTTING_DOWN, default_value=False)  # type: ignore

    @shutting_down.setter
    def shutting_down(self, value: bool) -> None:
        self._set_data(key=EDPCKeys.SHUTTING_DOWN, value=value, set_default_type=bool)

    def _th_logger(self) -> None:
        """Def th_logger - thread logs processor."""
        self.logger.info = "Starting logger worker"
        while not self.shutting_down:
            log = self.qlog.get(block=True)
            if log is None:
                break
            self.log_processor.send(log)

    def _th_worker(self) -> None:
        """Def th_worker - thread processor."""
        self.logger.info = "Starting worker..."
        idle: List[str] = [".", "..", "...", "...."]
        idle_idx = 0

        timestamp = Timestamp.now()

        while not self.shutting_down:
            idle_idx += 1
            if idle_idx >= len(idle):
                idle_idx = 0

            # processing queue
            timestamp: int = self.queue_processor(timestamp)
            try:
                if (
                    timestamp < Timestamp.now()
                    and self.config_dialog.status is not None
                ):
                    self.config_dialog.status["text"] = idle[idle_idx]
            except:
                pass

            if self.shutting_down:
                break

            time.sleep(1)

        self.logger.info = "Worker finished..."

    @property
    def qth(self) -> Union[Queue, SimpleQueue]:
        """Give me th queue."""
        return self._get_data(key=EDPCKeys.TH_QUEUE)  # type: ignore

    def queue_processor(self, timestamp: int) -> int:
        """Convert queue items."""
        time_break: int = 20
        test: bool = False

        # processing queue
        while not self.qth.empty() and not self.shutting_down:
            test = True
            self.logger.info = "Start processing the queue..."
            timestamp = Timestamp.now() + time_break
            try:
                item = self.qth.get(block=False)
                self.logger.debug = f"queue_processor: item = {item}"
                if item is None:
                    break
                if self.engine.convert(item):
                    # processing is done
                    if self.engine.has_messages():
                        for msg in self.engine.messages:
                            self.logger.info = msg
                            if self.config_dialog and self.config_dialog.status:
                                self.config_dialog.status["text"] = msg
                        self.engine.messages = None
                else:
                    # processing error
                    self.logger.error = "Image processing error"
                    if self.config_dialog and self.config_dialog.status:
                        self.config_dialog.status["text"] = "Image processing error"
                del item
            except Empty:
                continue
            except Exception as ex:
                self.logger.debug = f"Worker exception: {ex}"
                if self.config_dialog and self.config_dialog.status:
                    self.config_dialog.status["text"] = "ERROR: check logs"
                continue
            self.logger.info = "Done."
        if test:
            self.logger.debug = (
                f"queue_processor: queue empty, shut down time: {self.shutting_down}"
            )
        return timestamp


# #[EOF]#######################################################################
