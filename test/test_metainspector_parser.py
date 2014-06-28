# -*- coding: utf-8 -*-

"""
Unit test for pymetainspector: parser
"""

import unittest
from pymetainspector import metainspector
from test.fixtures import fixtures

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
        self.assertEqual(6, len(result.images), "Should find 6 images on twitter (image without src should be ignored")
        self.assertEqual("https://twimg0-a.akamaihd.net/profile_images/2380086215/fcu46ozay5f5al9kdfvq_reasonably_small.png; https://twimg0-a.akamaihd.net/profile_images/2380086215/fcu46ozay5f5al9kdfvq_normal.png; https://twimg0-a.akamaihd.net/profile_images/2293774732/v0pgo4xpdd9rou2xq5h0_normal.png; https://twimg0-a.akamaihd.net/profile_images/1538528659/jaime_nov_08_normal.jpg; https://si0.twimg.com/sticky/default_profile_images/default_profile_6_mini.png; https://twimg0-a.akamaihd.net/a/1342841381/images/bigger_spinner.gif",
                         "; ".join(result.images),
                         "Should find images on twitter")

    @fixtures.mockrequests
    def test_get_rss_feed(self):
        self.assertEqual("http://www.iteh.at/de/rss/",
                         metainspector.get("http://www.iteh.at").feed,
                         "Should get rss feed")
        self.assertEqual("http://www.tea-tron.com/jbravo/blog/feed/",
                         metainspector.get("http://www.tea-tron.com/jbravo/blog/").feed,
                         "Should get atom feed")
        self.assertIsNone(metainspector.get("http://www.alazan.com").feed,
                         "Should return None if no feed found")

    @fixtures.mockrequests
    def test_should_find_description(self):
        self.assertEqual("This is Youtube",
                         metainspector.get("http://www.youtube.com/watch?v=iaGSSrp49uc").description,
                         "Should find description from meta description")
        self.assertEqual("SAN FRANCISCO—In a move expected to revolutionize the mobile device industry, Apple launched its fastest and most powerful iPhone to date Tuesday, an innovative new model that can only be seen by the company's hippest and most dedicated customers. This is secondary text picked up because of a missing meta description.",
                         metainspector.get("http://theonion-no-description.com").description,
                         "Should find a secondary description if no meta description")

    



