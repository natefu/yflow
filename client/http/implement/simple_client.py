import logging
import requests
import time

from requests import Response
from requests.exceptions import RequestException
from typing import Optional

from utils import generate

logger = logging.getLogger()


class HttpClient:
    def __init__(
            self, method: str, url: str, payload: dict, headers: dict, timeout: Optional[int], form_urlencoded: bool,
            max_retry_attempts: int, min_retry_interval: int, max_retry_interval: int, log_id: str = None, **kwargs
    ) -> None:
        self.method = method
        self.url = url
        self.payload = payload
        self.headers = headers
        self.timeout = timeout
        self.form_urlencoded = form_urlencoded
        self.max_retry_attempts = max_retry_attempts
        self.min_retry_interval = min_retry_interval
        self.max_retry_interval = max_retry_interval
        self.log_id = log_id

    def request(self):
        self.build_headers()
        retry_attempt = 0
        while retry_attempt <= self.max_retry_attempts:
            try:
                response = self.make_request()
                print(response)
            except RequestException as e:
                logger.debug(f'request fail {e}')
            else:
                if response.ok:
                    return response
            retry_attempt += 1
            if retry_attempt <= self.max_retry_attempts:
                interval: int = self.get_retry_interval(retry_attempt=retry_attempt)
                time.sleep(interval)
        raise Exception(code=400, message='fail to make http requests')

    def make_request(self) -> Response:
        if self.form_urlencoded:
            return requests.request(
                self.method.upper(), self.url, data=self.payload, headers=self.headers, timeout=self.timeout
            )
        else:
            return requests.request(
                self.method.upper(), self.url, json=self.payload, headers=self.headers, timeout=self.timeout
            )

    def get_retry_interval(self, retry_attempt: int) -> int:
        return max(max(0, self.min_retry_interval), min(2**(retry_attempt-1), self.max_retry_interval))

    def build_headers(self) -> None:
        if not self.log_id:
            self.log_id = generate()
        if isinstance(self.headers, dict):
            self.headers.update({'x-tt-logid': self.log_id})
        else:
            self.headers = {'x-tt-logid': self.log_id}