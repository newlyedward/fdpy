import logging
from datetime import datetime
from typing import Any

from fdpy import database
from fdpy.event import EventEngine, Event
from .app import BaseApp
from .object import LogData
from .event import EVENT_LOG
from .utility import get_folder_path
from .setting import SETTINGS


class BaseEngine:
    """
    Abstract class for implementing an function engine.
    """

    def __init__(
            self,
            main_engine: Any,
            event_engine: EventEngine,
            engine_name: str,
    ):
        """"""
        self.main_engine = main_engine
        self.engine_name = engine_name

        if event_engine:
            self.event_engine = event_engine
        else:
            self.event_engine = EventEngine()

    def init_engine(self):
        """"""
        pass

    def start_engine(self):
        """"""
        pass

    def close_engine(self):
        """"""
        pass

    def register_event(self):
        """"""
        pass

    def process_event(self, event: Event):
        """"""
        pass

    def write_log(self, msg: str):
        """
        Put log event with specific message.
        :param msg:
        :return:
        """
        log = LogData(msg=msg)
        event = Event(EVENT_LOG, log)
        self.event_engine.put(event)


class MainEngine(BaseEngine):
    """
    Acts as the core engine.
    """

    def __init__(self, event_engine=EventEngine):
        """"""
        super(MainEngine, self).__init__(self, event_engine, "main")

        self.engines = {}
        self.apps = {}
        self.db = database.connect('finance')

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

    def start_engine(self):
        """"""
        self.event_engine.start()

    def write_log(self, msg: str):
        """
        Put log event with specific message.
        :param msg:
        :return:
        """
        log = LogData(msg=msg)
        event = Event(EVENT_LOG, log)
        self.event_engine.put(event)

    def get_engine(self, engine_name: str):
        """
        Return engine object by name.
        :param engine_name:
        :return:
        """
        engine = self.engines.get(engine_name, None)
        if not engine:
            self.write_log(f"Can't find engine: {engine_name}")
        return engine

    def add_app(self, app_class: BaseApp):
        """
        Add app.
        :param app_class:
        :return:
        """
        app = app_class()
        self.apps[app.app_name] = app

        engine = self.add_engine(app.engine_class)
        return engine

    def close_engine(self):
        """
        Make sure every gateway and app is closed properly before
        programme exit.
        """
        # Stop event engine first to prevent new timer event.
        self.event_engine.stop()

        for engine in self.engines.values():
            engine.close_egine()


class LogEngine(BaseEngine):
    """
    Process log event and output with logging module.
    """

    def __init__(
            self,
            main_engine: MainEngine,
            event_engine: EventEngine
    ):
        super(LogEngine, self).__init__(main_engine, event_engine, "log")

        if not SETTINGS["log.active"]:
            return

        self.level = SETTINGS["log.level"]

        self.logger = logging.getLogger("FD Collector")
        self.logger.setLevel(self.level)

        self.formatter = logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s"
        )

        self.add_null_handler()

        if SETTINGS["log.console"]:
            self.add_console_handler()

        if SETTINGS["log.file"]:
            self.add_file_handler()

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
        self.event_engine.register(EVENT_LOG, self.process_event)

    def process_event(self, event: Event):
        """
        Process log event.
        :param event:
        :return:
        """
        log = event.data
        self.logger.log(log.level, log.msg)
