# -*- coding: utf-8 -*-

"""
Unit test for pymetainspector: parser
"""

import unittest, requests
from pymetainspector import metainspector
from test.fixtures import fixtures
from datetime import datetime
class ParserTest(unittest.TestCase):
    @fixtures.mockrequests
    def test_basic_scrape_hastitle_noimage(self):
        result = metainspector.get("http://pagerankalert.com")

        #has: title, no: og:image
        self.assertEqual("PageRankAlert.com :: Track your PageRank changes & receive alerts",
                         result.title, "Should get the title")
        self.assertIsNone(result.image, "Should not find an image")

    @fixtures.mockrequests
    def test_should_find_og_image(self):
        #has: og:image
        self.assertEqual("http://o.onionstatic.com/images/articles/article/2772/Apple-Claims-600w-R_jpg_130x110_q85.jpg",
                         metainspector.get("http://www.theonion.com/articles/apple-claims-new-iphone-only-visible-to-most-loyal,2772/").image,
                         "Should find the og:image")

        self.assertEqual("http://i2.ytimg.com/vi/iaGSSrp49uc/mqdefault.jpg",
                         metainspector.get("http://www.youtube.com/watch?v=iaGSSrp49uc").image,
                         "Should find image on youtube")

    @fixtures.mockrequests
    def test_should_find_all_page_images(self):
        self.assertEqual(['http://pagerankalert.com/images/pagerank_alert.png?1305794559'],
                         metainspector.get("http://pagerankalert.com").images,
                         "Should find all page images")

        result = metainspector.get("https://twitter.com/markupvalidator")
        self.assertEqual(6, len(result.images), "Should find 6 images on twitter")
        self.assertEqual("https://twimg0-a.akamaihd.net/profile_images/2380086215/fcu46ozay5f5al9kdfvq_reasonably_small.png; https://twimg0-a.akamaihd.net/profile_images/2380086215/fcu46ozay5f5al9kdfvq_normal.png; https://twimg0-a.akamaihd.net/profile_images/2293774732/v0pgo4xpdd9rou2xq5h0_normal.png; https://twimg0-a.akamaihd.net/profile_images/1538528659/jaime_nov_08_normal.jpg; https://si0.twimg.com/sticky/default_profile_images/default_profile_6_mini.png; https://twimg0-a.akamaihd.net/a/1342841381/images/bigger_spinner.gif",
                         "; ".join(result.images),
                         "Should find images on twitter")

