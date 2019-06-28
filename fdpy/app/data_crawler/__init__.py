from pathlib import Path

from fdpy.processor.app import BaseApp

from .base import APP_NAME
from .engine import CrawlerEngine


class CrawlerApp(BaseApp):
    """"""

    app_name = APP_NAME
    app_module = __module__
    app_path = Path(__file__).parent
    engine_class = CrawlerEngine
