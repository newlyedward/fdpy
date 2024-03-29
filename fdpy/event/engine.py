"""
Event-driven framework
"""

from collections import defaultdict
from queue import Empty, Queue
from threading import Thread
from time import sleep
from typing import Any, Callable

EVENT_TIME = "eTimer"


class Event:
    """
    Event object consists of a type string which is used by event engine for distributing event,
    and a data object which contains the real data.
    """

    def __init__(self, type: str, data: Any = None, callback: Callable[[], None] = None):
        """"""
        self.type = type
        self.data = data
        self.callback = callback


HandlerType = Callable[[Event], None]


class EventEngine:
    """
    Event engine distributes event object based on its type to those handlers registered.

    It also generates timer event by every interval seconds, which can be used for timing purpose.
    """

    def __init__(self, interval: int = 1):
        """
        Timer event is generated every 1 second by default, if interval not specified.
        :param interval: int, interval time
        """
        self._interval = interval
        self._queue = Queue()
        self._active = False
        self._thread = Thread(target=self._run)
        self._timer = Thread(target=self._run_timer)
        self._handlers = defaultdict(list)
        self._general_handlers = []

    def _run(self):
        """
        Get event from queue and then process it.
        :return:
        """
        while self._active:
            try:
                event = self._queue.get(block=True, timeout=1)
                self._process(event)
            except Empty:
                pass

    def _process(self, event: Event):
        """
        First distribute event to those handlers register listening to this type.

        Then distribute event to those general handlers which listens to all types.
        :param event:
        :return:
        """
        if event.type in self._handlers:
            [handler(event) for handler in self._handlers[event.type]]

        if self._general_handlers:
            [handler(event) for handler in self._general_handlers]

    def _run_timer(self):
        """
        Sleep by interval second(s) and then generate a timer event.
        :return:
        """
        while self._active:
            sleep(self._interval)
            event = Event(EVENT_TIME)
            self.put(event)

    def start(self):
        """
        Start event engine to process events and generate timer events.
        :return:
        """
        self._active = True
        self._thread.start()
        self._timer.start()

    def stop(self):
        """
        Stop event engine.
        :return:
        """
        self._active = False
        self._timer.join()
        self._thread.join()

    def put(self, event: Event):
        """
        Put an event object into event queue.
        :param event:
        :return:
        """
        self._queue.put(event)

    def register(self, type: str, handler: HandlerType):
        """
        Register a new handler function for a specific event type.
        Every function can only be registered once for each event type.
        :param type:
        :param handler:
        :return:
        """
        handler_list = self._handlers[type]
        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, type: str, handler: HandlerType):
        """
        Unregister an existing handler function from event engine.
        :param type:
        :param handler:
        :return:
        """
        handler_list = self._handlers[type]

        if handler in handler_list:
            handler_list.remove(handler)

        if not handler_list:
            self._handlers.pop(type)

    def register_general(self, handler: HandlerType):
        """
        Register a new handler function for all event types. Every
        function can only be registered once for each event type.
        """
        if handler not in self._general_handlers:
            self._general_handlers.append(handler)

    def unregister_general(self, handler: HandlerType):
        """
        Unregister an existing general handler function.
        """
        if handler in self._general_handlers:
            self._general_handlers.remove(handler)
