import multiprocessing
from time import sleep
from datetime import datetime, time, timedelta
from logging import INFO

from fdpy.event import EventEngine
from fdpy.processor.setting import SETTINGS

SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
SETTINGS["log.console"] = True
SETTINGS["log.file"] = True


def main():
    event_engin = EventEngine()
    main_engin = MainEngin(event_engin)

def run_parent():
    """
    Running in the parent process
    :return: 
    """
    print('Start financial data collector daemon.')

    # Chinese futures market trading period (day/night)
    DAY_START = time(8, 45)
    DAY_END = time(15, 30)

    NIGHT_START = time(20, 45)
    NIGHT_END = time(2, 45)

    child_process = None

    while True:
        current_time = datetime.now()

        if (
                (DAY_END + timedelta(hours=1) < current_time < NIGHT_START)
                or (NIGHT_END + timedelta(hours=1) < current_time < DAY_START)
        ):
            collecting = True

        if collecting and child_process is None:
            print("Start child process!")
            child_process = multiprocessing.Process(target=run_child)
            child_process.start()
            print("Start child process successfully!")

        if not collecting and child_process is not None:
            print("Close child process!")
            child_process.terminate()
            child_process.join()
            child_process = None
            print("Close child process successfully!")

        sleep(5)


if __name__ == "__main__":
    run_parent()