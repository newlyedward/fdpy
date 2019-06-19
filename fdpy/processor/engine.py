import logging
from abc import ABC
from datetime import datetime
from typing import Any

from fdpy.event import EventEngine, Event
from .event import EVENT_LOG
from .utility import get_folder_path
from .setting import SETTINGS


class MainEngine:
    """
    Acts as the core engine.
    """

    def __init__(self, event_engine: EventEngine = None):
        """"""
        if event_engine:
            self.event_engine = event_engine
        else:
            self.event_engine = EventEngine()
        self.event_engine.start()

        self.gateways = {}
        self.engines = {}
        self.apps = {}
        self.exchanges = []

        self.init_engines()

    def add_engines(self, engine_class: Any):
        """
        Add function engine.
        :param engine_class:
        :return:
        """
        engine = engine_class(self, self.event_engine)
        self.engines[engine.engine_name] = engine
        return engine

    def init_engines(self):
        """
        Init all engines.
        :return:
        """
        self.add_engines(LogEngine)

    def write_log(self, msg: str, source: str = ""):
        """
        Put log event with specific message.
        :param msg:
        :param source:
        :return:
        """
        log = LogData


class BaseEngine(ABC):
    """
    Abstract class for implementing an function engine.
    """

    def __init__(
            self,
            main_engine: MainEngine,
            event_engine: EventEngine,
            engine_name: str,
    ):
        """"""
        self.main_engine = main_engine
        self.event_engine = event_engine
        self.engine_name = engine_name

    def close(self):
        """"""
        pass


class LogEngine(BaseEngine):
    """
    Porcess log event and output with logging module.
    """

    def __init__(
            self,
            main_engine: MainEngine,
            event_engine: EventEngine
    ):
        super(LogEngine, self).__init__(main_engine, event_engine, "log")

        if SETTINGS["log.active"]:
            return

        self.level = SETTINGS["log.level"]

        self.logger = logging.getLogger("FD Collector")
        self.logger.setLevel(self.level)

        self.formatter = logging.Formatter(
            "%(asctime) %(levelname)s: %(message)s"
        )

        self.add_null_handler()

        if SETTINGS["log.console"]:
            self.add_console_handler()

        if SETTINGS["log.file"]:
            self.add_console_handler()

        self.register_event()

    def add_null_handler(self):
        """
        add null handler for logger.
        :return:
        """
        null_handler = logging.NullHandler()
        self.logger.addHandler(null_handler)

    def add_console_handler(self):
        """
        Add console output of log.
        :return:
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def add_file_handler(self):
        today_date = datetime.now().strftime("%Y%m%d")
        filename = f"fd_{today_date}.log"
        log_path = get_folder_path('log')
        file_path = log_path.joinpath(filename)

        file_handler = logging.FileHandler(
            file_path, mode="a", encoding="utf8"
        )
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def register_event(self):
        """"""
        self.event_engine.register(EVENT_LOG, self.process_log_event)

    def process_log_event(self, event:Event):
        """
        Process log event.
        :param event:
        :return:
        """
        log = event.data
        self.logger.log(log.level, log.msg)

