from orderedset._orderedset import OrderedSet
from pymetainspector.pageurl import PageURL
from pyquery import PyQuery

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
        self.meta_keywords = None
        self.meta_description = None
        self.description = None
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
        Parse meta from pyquery object : default to None if not found

        :param PyQuery pqobject : PyQuery object
        """
        #Fetch: page title from <title>...</title>
        self.title = pqobject("title").text() or None

        #Fetch: <meta property="og:image" content="...">
        self.image = pqobject("meta[property='og:image']:first").attr("content") or None

        #Fetch: list of <img src="...">
        self.images = [self.to_absolute_url(imgsrc) for imgsrc in
                       OrderedSet([(img.get("src")) for img in pqobject("img") if img.get("src")])] or None

        #Fetch: rss feed
        feed = pqobject("""[type='application/rss+xml']:first,[type='application/atom+xml']:first""").attr("href")
        feed = self.to_absolute_url(feed) if feed else None
        self.feed = feed
