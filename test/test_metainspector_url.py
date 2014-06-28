# -*- coding: utf-8 -*-

"""
Unit test for pymetainspector: url
"""

import unittest, requests
from pymetainspector import metainspector
from test.fixtures import fixtures

ignore_ssl_request_function = lambda url: requests.get(url, verify=False)

class UrlTest(unittest.TestCase):
    @fixtures.mockrequests
    def test_should_normalize_urls(self):
        self.assertEqual("http://example.com/", metainspector.get("http://example.com").url, "Should normalize URLs")

    @fixtures.mockrequests
    def test_should_accept_an_url_with_scheme(self):
        self.assertEqual("http://example.com/", metainspector.get("http://example.com/").url,
                         "Should accept an URL with scheme")
        self.assertEqual("https://example.com/",
                         metainspector.get("https://example.com/", request_function=ignore_ssl_request_function).url,
                         "Should accept an URL with scheme")

    @fixtures.mockrequests
    def test_should_use_http_as_default_scheme(self):
        self.assertEqual("http://example.com/", metainspector.get("example.com").url,
                         "Should use http:// as a default scheme")
        self.assertEqual("http://example.com/", metainspector.get("//example.com").url,
                         "Should use http:// as a default scheme on omitted scheme url")

    @fixtures.mockrequests
    def test_should_accept_url_with_international_characters(self):
        self.assertEqual("http://www.international.com/ol%C3%A9",
                         metainspector.get("http://www.international.com/olé").url,
                         "Should accept an URL with international characters")

    @fixtures.mockrequests
    def test_should_return_the_scheme(self):
        self.assertEqual("http", metainspector.get("http://example.com").scheme, "Should return the scheme")
        self.assertEqual("https",
                         metainspector.get("https://example.com/", request_function=ignore_ssl_request_function).scheme,
                         "Should return the scheme")
        self.assertEqual("http", metainspector.get("example.com").scheme, "Should return the scheme")

    @fixtures.mockrequests
    def test_should_return_the_host(self):
        self.assertEqual("example.com", metainspector.get("http://example.com").host, "Should return the host")
        self.assertEqual("example.com",
                         metainspector.get("https://example.com/", request_function=ignore_ssl_request_function).host,
                         "Should return the host")
        self.assertEqual("example.com", metainspector.get("example.com").host, "Should return the host")

    @fixtures.mockrequests
    def test_should_return_the_root_url(self):
        self.assertEqual("http://example.com/", metainspector.get("http://example.com").root_url, "Should return the root url")
        self.assertEqual("https://example.com/",
                         metainspector.get("https://example.com/", request_function=ignore_ssl_request_function).root_url,
                         "Should return the root url")
        self.assertEqual("http://example.com/", metainspector.get("example.com").root_url, "Should return the root url")
        self.assertEqual("http://example.com/", metainspector.get("http://example.com/faqs").root_url, "Should return the root url")

    @fixtures.mockrequests
    def test_edit_url_should_update_the_url(self):
        page = metainspector.get("http://first.com")
        page.url = "https://second.com/"
        self.assertEqual("https://second.com/", page.url, "Should update the url")
        self.assertEqual("https", page.scheme, "Should update the scheme")
        self.assertEqual("second.com", page.host, "Should update the host")
        self.assertEqual("https://second.com/", page.root_url, "Should update the root url")

    @fixtures.mockrequests
    def test_edit_url_should_add_missing_scheme_and_normalize(self):
        page = metainspector.get("http://first.com")
        page.url = "second.com"
        self.assertEqual("http://second.com/", page.url, "Should add the missing scheme and normalize")
