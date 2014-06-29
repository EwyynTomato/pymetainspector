from collections import namedtuple
from orderedset._orderedset import OrderedSet
from pymetainspector.pageurl import PageURL
from pyquery import PyQuery
import logging, lxml

try: #Python 3 import
    from urllib.parse import urlparse, urlunparse, urljoin
except ImportError: #Fallback to Python 2
    from urlparse import urlparse, urlunparse, urljoin

class Page(PageURL):
    def __init__(self):
        super().__init__()
        self.title = None # Text value of <title>, this is different from <meta property="og:title">
        self.links = None
        self.internal_links = None
        self.external_links = None
        self.author = None
        self.meta = None
        self.meta_tags = None
        self.description = None # Returns <meta name="description" content="...">, or the first long paragraph if no meta description is found
        self.image = None  # Value of content from 1st : <meta property="og:image" content="...">
        self.images = None # List of absolute url from <img src="..." />, in which the value of src shouldn't be empty
        self.feed = None # RSS feed on this page
        self.charset = None
        self.content_type = None

    def from_html(self, html_string):
        """
        Parse meta from pyquery object

        :param PyQuery html_string : str
        """
        pyquery_object = PyQuery(html_string)
        self.from_pyquery(pyquery_object)

    def from_pyquery(self, pqobject):
        """
        Parse meta from pyquery object : values default to None if not found

        :param PyQuery pqobject : PyQuery object
        """
        pqmeta = PyQuery(pqobject("meta"))

        #Fetch meta
        (self.meta_tags, self.meta) = self.get_meta(pqmeta)

        #Fetch: page title from <title>...</title>
        self.title = pqobject("title").text() or None

        #Fetch: <meta property="og:image" content="...">
        self.image = pqmeta("[property='og:image']").attr("content") or None

        #Fetch: list of <img src="...">, return them as absolute url
        self.images = [self.to_absolute_url(imgsrc) for imgsrc in
                       OrderedSet([(img.get("src")) for img in pqobject("img") if img.get("src")])] or None

        #Fetch: rss/atom feed
        feed = pqobject("""[type='application/rss+xml']:first,[type='application/atom+xml']:first""").attr("href")
        feed = self.to_absolute_url(feed) if feed else None
        self.feed = feed

        #Fetch: description, <meta name="description" content="...">
        #TODO: Should description also include og description? e.g. StackOverflow
        self.description = pqmeta("[name='description']").attr("content")
        if not self.description:
            long_p_elements  = pqobject[0].xpath("(//p[string-length() >= 120])[1]") #PyQuery doesn't support xpath selector,
                                                                                     # so we directly use its lxml object here.
            self.description = long_p_elements[0].text if len(long_p_elements) > 0 else None

    @staticmethod
    def get_meta(pqmeta):
        """
        Return PyQuery meta node into:
            1. full dictionary of meta tags' attribute and their corresponding content
            2. flat dictionary form of meta attributes and their content

        :param PyQuery pqmeta : PyQuery containing only meta tags
        :rtype: _MetaStruct
        """
        meta_tags = {}
        meta_short = {}
        for meta in pqmeta: #: type meta: lxml.html.HtmlElement
            try:
                metadict = dict(meta.items())
                metacontent = metadict.pop("content")
                for attribute in metadict:
                    attribute_value = metadict[attribute]
                    metadict[attribute] = { attribute_value : metacontent }
                    meta_short[attribute_value] = metacontent
                meta_tags.update(metadict)
            except (KeyError, IndexError):
                logging.warning("Malformed meta : %s" % lxml.html.tostring(meta))

        return _MetaStruct(meta_tags, meta_short)


_MetaStruct = namedtuple("_MetaStruct", "meta_tags meta_short")


