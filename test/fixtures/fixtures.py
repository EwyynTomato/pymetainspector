# -*- coding: utf-8 -*-

"""
Fixtures: mock response for unit test
"""

from os import path
from httmock import urlmatch, HTTMock

folder = "test/fixtures"
def get_file_path(filename):
    return path.join(folder, filename)


with open(get_file_path("example.com.html")) as f:
    html_example = f.read()

    @urlmatch(netloc=r"example.com")
    def response_content(url, request):
        return {'status_code': 200, 'content': str.encode(html_example)}


with open(get_file_path("empty.html")) as f:
    html_empty = f.read()

    @urlmatch(netloc=r"(.*\.?)(?:international|first)\.com$")
    def empty_content(url, request):
        return {'status_code': 200, 'content': str.encode(html_empty)}


def mockrequests(f):
    def inner(*args, **kwargs):
        with HTTMock(response_content, empty_content):
            return f(*args, **kwargs)
    return inner


