# -*- coding: utf-8 -*-

"""
Fixtures: mock response for unit test
"""

from os import path
from httmock import urlmatch, HTTMock

class _Fixtures(object):
    def __init__(self):
        self.html_folder = "test/fixtures/html"

        # Add mock response - hostname pair for our mock response
        self.mock_response_function_list = []
        self.add_mock_response_from_html_and_netloc("example.com.html", "example.com")
        self.add_mock_response_from_html_and_netloc("empty.html", "(.*\.?)(?:international|first)\.com$")
        self.add_mock_response_from_html_and_netloc("pagerankalert.com.html", "(.*\.?)pagerankalert\.com")
        self.add_mock_response_from_html_and_netloc("theonion.com.html", "(.*\.?)theonion\.com(.*)")
        self.add_mock_response_from_html_and_netloc("youtube.com.html", "(.*\.?)youtube\.com(.*)")
        self.add_mock_response_from_html_and_netloc("twitter.com.html", "(.*\.?)twitter\.com(.*)")
        self.add_mock_response_from_html_and_netloc("iteh.at.html", "(.*\.?)iteh\.at(.*)")
        self.add_mock_response_from_html_and_netloc("tea-tron.com.html", "(.*\.?)tea-tron\.com(.*)")
        self.add_mock_response_from_html_and_netloc("alazan.com.html", "(.*\.?)alazan\.com(.*)")

    def add_mock_response_from_html_and_netloc(self, html_filepath, netloc_regex):
        self.add_mock_response_function_list(self.get_mock_request_function(html_filepath, netloc_regex))

    def add_mock_response_function_list(self, mock_request_function):
        """
        Add mock request function
        :param function mock_request_function : See function get_mock_request_function for example
        """
        self.mock_response_function_list.append(mock_request_function)

    def get_html_file_path(self, filename):
        """
        Simply join path and filename, e.g. empty.html -> test/fixtures/html/empty.html

        :param str filename : html filename
        """
        return path.join(self.html_folder, filename)

    def get_mock_request_function(self, html_file, urlmatch_regex):
        """
        Return a function for our mock request, matching given url regex

        :param str html_file : html file containing our mock response
        :param str urlmatch_regex : netlock regex for HTTMock
        :
        """
        with open(self.get_html_file_path(html_file)) as f:
            html_example = f.read()

            @urlmatch(netloc=urlmatch_regex)
            def response_function(url, request):
                return {'status_code': 200, 'content': str.encode(html_example)}

        return response_function

_httmock_mock_response_function_list = _Fixtures().mock_response_function_list

def mockrequests(func):
    """
    Fixture decorator function
    """
    def inner(*args, **kwargs):
        with HTTMock(*_httmock_mock_response_function_list):
            return func(*args, **kwargs)
    return inner


