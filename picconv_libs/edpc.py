# -*- coding: UTF-8 -*-
"""
  edpc.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 14.01.2024, 18:01:41
  
  Purpose: EDPC main class.
"""


from picconv_libs.base_log import BLogClient, BLogProcessor
from picconv_libs.converter import PicConverter
from picconv_libs.dialogs import ConfigDialog
from picconv_libs.system import LogClient, LogProcessor


from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise


from inspect import currentframe
import time
from queue import Queue, SimpleQueue, Empty
from threading import Thread
from typing import List, Union


class EDPC(BLogProcessor, BLogClient, NoDynamicAttributes):
    """edpc_object main class."""

    __pluginname: str = None  # type: ignore
    __shutting_down: bool = False

    __th_queue: Union[Queue, SimpleQueue] = None  # type: ignore
    __th_worker: Thread = None  # type: ignore

    config_dialog: ConfigDialog = None  # type: ignore
    engine: PicConverter = None  # type: ignore

    def __init__(self) -> None:
        """Initialize main class."""
        self.shutting_down = False

        self.pluginname = "EDPC"
        version = "0.3.9"

        # logging subsystem
        self.qlog = SimpleQueue()
        self.log_processor = LogProcessor(self.pluginname)
        self.logger = LogClient(self.qlog)

        # logging thread
        self.th_log = Thread(
            target=self.th_logger, name=f"{self.pluginname} log worker", daemon=True
        )
        self.th_log.start()

        # config dialog
        self.config_dialog = ConfigDialog(self.qlog)
        self.config_dialog.pluginname = self.pluginname
        self.config_dialog.version = version

        # worker thread
        self.thworker = Thread(
            target=self.th_worker,
            name=f"{self.config_dialog.pluginname} worker",
            daemon=True,
        )

        self.__th_queue = SimpleQueue()
        self.engine = PicConverter(self.qlog)
        self.engine.has_pillow()

    @property
    def thworker(self) -> Thread:
        """Give me access to thworker variable."""
        return self.__th_worker

    @thworker.setter
    def thworker(self, value: Thread) -> None:
        self.__th_worker = value

    @property
    def pluginname(self) -> str:
        """Give me access to pluginname variable."""
        if self.__pluginname is None:
            self.__pluginname = ""
        return self.__pluginname

    @pluginname.setter
    def pluginname(self, value: str) -> None:
        self.__pluginname = value

    @property
    def shutting_down(self) -> bool:
        """Give me access to shutting_down flag."""
        return self.__shutting_down

    @shutting_down.setter
    def shutting_down(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise Raise.error(
                f"Boolean type expected, '{type(value)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self.__shutting_down = value

    def th_logger(self) -> None:
        """Def th_logger - thread logs processor."""
        self.logger.info = "Starting logger worker"
        while not self.shutting_down:
            log = self.qlog.get(block=True)
            if log is None:
                break
            self.log_processor.send(log)

    def th_worker(self) -> None:
        """Def th_worker - thread processor."""
        self.logger.info = "Starting worker..."
        idle: List[str] = [".", "..", "...", "...."]
        idle_idx = 0

        timestamp = int(time.time())

        while not self.shutting_down:
            idle_idx += 1
            if idle_idx >= len(idle):
                idle_idx = 0

            # processing queue
            timestamp: int = self.queue_processor(timestamp)
            try:
                if (
                    timestamp < int(time.time())
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
        return self.__th_queue

    def queue_processor(self, timestamp: int) -> int:
        """Convert queue items."""
        time_break: int = 20
        test: bool = False

        # processing queue
        while not self.qth.empty() and not self.shutting_down:
            test = True
            self.logger.info = "Start processing the queue..."
            timestamp = int(time.time()) + time_break
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
