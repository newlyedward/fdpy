"""spiders for websites"""
from dataclasses import dataclass
from typing import Any
from datetime import date

from pymongo import DESCENDING

from fdpy.app.data_crawler.http import Request


@dataclass
class Domain:
    """Abstract class to contain spiders"""
    name: str = ""  # website
    allowed_domains: str = ""
    db: Any = None
    spiders: list = None


class Spider:
    """
    Spider for only one kind of data.
    """
    name = ""  # data type
    url_templates = {}
    file_dir = ""

    def __init__(self, domain: Domain):
        self.domain = domain
        self.cursor = self.domain.db[self.name]

    def start_requests(self) -> Request:
        """According to files and trade calender to decide url"""
        filer_dict = {"market": self.domain.name}
        projection = {"_id": 0, "datetime": 1}

        start = self.cursor.find_one(filer_dict, projection=projection, sort=[("datetime", DESCENDING)])

    # get files
    # get calender
    # yield url request

    def parse(self):
        """"""
        pass
    # get last records
    # get calender
    # calculate the data needed to insert to database
    # covert data for database
    # yield insert request event
