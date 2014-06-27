# -*- coding: utf-8 -*-

"""
pymetainspector.MetaInspector
-------------------
"""

try: #Python 3 import
    from urllib.parse import urlparse
except ImportError: #Fallback to Python 2
    from urlparse import urlparse

import requests
from pyquery import PyQuery
from .page import Page


def default_request_function(url):
    """
    :rtype: requests.Response
    """
    return requests.get(url)


def get(url, request_function=default_request_function):
    """
    :param str url : perform a GET request for this url, and retrieve its meta information
    :param function request_function : (optional) Function that should return :rtype: request.Response,
                                       define another function if you need requests to have options

    Usage 1:
    >>> from pymetainspector import metainspector
    >>> result = metainspector.get("http://www.example.com")

    Usage 2 - Ignore ssl error by passing custom request function :
    >>> from pymetainspector import metainspector
    >>> import requests
    >>> ignore_ssl_request_function = lambda url: requests.get(url, verify=False)
    >>> result = metainspector.get("https://www.example.com", request_function=ignore_ssl_request_function)

    :rtype: Page
    """
    if not urlparse(url).scheme:
        # Should use http:// scheme by default
        url = "http://%s" % url

    working_response = request_function(url)
    """@type : requests.Response"""

    return parse(html_string=working_response.text, url=working_response.url)


def parse(html_string, url=None):
    """
    Retrieve meta information from given html string

    :param str html_string : the source html
    :param str url : (optional) the url for the html

    :rtype: Page
    """
    working_page = Page()

    if url:
        working_page.url = url

    dom = PyQuery(html_string)
    working_page.title = dom("title").text()

    return working_page







