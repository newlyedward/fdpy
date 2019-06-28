import requests
from requests import RequestException

from fdpy.event import EventEngine, Event
from fdpy.processor.engine import BaseEngine, MainEngine

from .base import APP_NAME

EVENT_REQUEST = "eRequest"
EVENT_RESPONSE = "eResponse"
EVENT_READ = "eRead"


class CrawlerEngine(BaseEngine):
    """"""

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        super(CrawlerEngine).__init__(
            main_engine, event_engine, APP_NAME
        )

        self.domains = []           # according to websites

    def init_engine(self):
        """"""

        self.register_event()
        self.write_log("Start crawler engine successfully!")

    def start_engine(self):
        for domain in self.domains:
            for spider in domain:
                for request in iter(spider.start_requests()):
                    event = Event(EVENT_REQUEST, request)
                    self.event_engine.put(event)

    def process_request(self, event: Event):
        """
        Get data from url
        :param event:
        :return: response
        """
        request = event.data

        if request.method == "GET":
            try:
                response = requests.get(
                    request.url, headers=request.headers, timeout=request.timeout)
            except RequestException as e:
                self.write_log(f"Unable to get page content: {e}")
                return
        elif request.method == "POST":
            try:
                response = requests.post(
                    request.url, data=request.data, headers=request.headers, timeout=request.timeout)
            except RequestException as e:
                self.write_log(f"Unable to get page content: {e}")
                return
        elif request.method == "READ":
            event = Event(type=EVENT_READ, data=None, callback=request.callback)
            self.event_engine.put(event)
        else:
            self.write_log(f"Not support request method: {request.method}")
            return

        if request.encoding:
            response.encoding = request.encoding

        event = Event(type=EVENT_RESPONSE, data=response, callback=request.callback)
        self.event_engine.put(event)

    def process_response(self, event: Event):
        """
        Get data from url
        :param event:
        :return: response
        """
        response = event.data
        # save
        pass

    def process_read(self, event: Event):
        """
        Get data from url
        :param event:
        :return: response
        """
        response = event.data
        # save
        pass


    def register_event(self):
        """"""
        self.event_engine.register(EVENT_REQUEST, self.process_request)
        self.event_engine.register(EVENT_RESPONSE, self.process_response)
        self.event_engine.register(EVENT_READ, self.process_read)
