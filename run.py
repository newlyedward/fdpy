import multiprocessing
from time import sleep
from datetime import datetime, time, timedelta
from logging import INFO

from fdpy.event import EventEngine, EVENT_TIME, Event
from fdpy.processor.setting import SETTINGS
from fdpy.processor.engine import MainEngine

SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
SETTINGS["log.console"] = True
SETTINGS["log.file"] = True


def main():
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.write_log("Create main engine successfully!")

    def current(event: Event):
        main_engine.write_log(f"{event.type}")

    event_engine.register(EVENT_TIME, current)

    main_engine.start_engine()
    sleep(10)


if __name__ == "__main__":
    main()
