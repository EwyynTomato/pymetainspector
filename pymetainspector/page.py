from orderedset._orderedset import OrderedSet
from pymetainspector.pageurl import PageURL

try: #Python 3 import
    from urllib.parse import urlparse, urlunparse, urljoin
except ImportError: #Fallback to Python 2
    from urlparse import urlparse, urlunparse, urljoin

class Page(PageURL):
    def __init__(self):
        super().__init__()
        self.title = None
        self.links = None
        self.internal_links = None
        self.external_links = None
        self.author = None
        self.meta_keywords = None
        self.meta_description = None
        self.description = None
        self.image = None
        self.images = None
        self.feed = None
        self.charset = None
        self.content_type = None

    def from_pyquery(self, pqobject):
        """
        Parse meta from pyquery object : default to None if not found
        """
        self.title = pqobject("title").text() or None
        self.image = pqobject("meta[property='og:image']:first").attr("content") or None
        self.images = [self.to_absolute_url(imgsrc) for imgsrc in
                       OrderedSet([(img.get("src")) for img in pqobject("img") if img.get("src")])] or None
