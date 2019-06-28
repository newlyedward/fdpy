import requests
from requests.exceptions import RequestException
from dataclasses import dataclass
from typing import Callable, Any

from fdpy.event import Event

HEADERS = {'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           }


def get_html_text(url, headers=None, encoding=None):
    if headers is None:
        headers = HEADERS

    try:
        response = requests.get(url, headers=headers, timeout=30)
    except RequestException as e:
        return f"Unable to get page content: {e}"

    if encoding is None:
        response.encoding = response.apparent_encoding
    else:
        response.encoding = encoding

    return response.text


@dataclass
class Request:
    """"""
    method: str
    url: str
    params: dict = None
    data: dict = None
    headers: dict = None
    timeout: int = 3
    encoding: str = "utf8"
    callback: Callable[[Event], None] = None

    def __post_init__(self):
        """"""
        self.method = self.method.upper()
        if self.headers is None:
            self.headers = HEADERS
