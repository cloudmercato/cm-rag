from urllib.parse import urljoin
from django.conf import settings

import requests
from requests.auth import AuthBase
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class CtpError(Exception):
    pass


class CtpAuth(AuthBase):
    def __call__(self, request):
        request.headers['Ctp-Token'] = settings.CTP_TOKEN
        return request


class CtpClient:
    def __init__(self):
        self.url = settings.SOURCE_URL
        self.session = requests.Session()
        retry = Retry(**settings.SOURCE_RETRY)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.hooks['response'].append(self._handle_response)

    def _handle_response(self, response, *args, **kwargs):
        if response.status_code >= 300:
            raise CtpError(response)
        return response

    def get(self, url, params=None):
        full_url = urljoin(self.url, url)
        return self.session.get(full_url, json=params)

    def query(self, q):
        url = self.url
        response = self.get(url)
        response_json = response.json()
        answer = response_json['answer']
        return answer
