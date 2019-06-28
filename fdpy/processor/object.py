from dataclasses import dataclass
from datetime import datetime
from logging import INFO


@dataclass
class LogData:
    """
    Log data is used for recording log messages on GUI or in log files
    """
    msg: str
    level: int = INFO

    def __post_init__(self):
        """"""
        self.time = datetime.now()
