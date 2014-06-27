try: #Python 3 import
    from urllib.parse import urlparse, urlunparse
except ImportError: #Fallback to Python 2
    from urlparse import urlparse, urlunparse

class Page(object):
    """
    Result object containing information from inspected url/html
    """

    def __init__(self):
        self._url = ""
        self._scheme = ""
        self._host = ""
        self._root_url = ""
        self.title = ""
        self.links = ""
        self.internal_links = ""
        self.external_links = ""
        self.author = ""
        self.meta_keywords = ""
        self.meta_description = ""
        self.description = ""
        self.image = ""
        self.images = ""
        self.feed = ""
        self.charset = ""
        self.content_type = ""

    def __repr__(self):
        return "<Page : %s>" % self.__dict__

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, val):
        """
        Parse url and set the url info into Page's object instances

        :type val : str
        """
        if not urlparse(val).scheme:
            val = "http://%s" % val # Should use http:// scheme by default
        parsed_url = urlparse(val)
        """:type parsed_url : ParseResult"""

        #- Set: url, scheme, host, root_url
        self._scheme = parsed_url.scheme if parsed_url.scheme else "http" #Should default to "http"
        self._host = parsed_url.hostname
        self._root_url = urlunparse((parsed_url.scheme, parsed_url.netloc, "/", '', '', ''))
        normalized_path = parsed_url.path if parsed_url.path else "/"
        self._url = urlunparse((self._scheme, self.host, normalized_path,
                                parsed_url.params, parsed_url.query, parsed_url.fragment))


    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, val):
        """
        Update scheme
        Should update:
            1. url
            2. scheme
            3. root_url

        :type val : str
        """
        parsed_origin_url = urlparse(self.url)
        """:type : ParseResult"""

        #update url: scheme & root_url will also be updated here
        self.url = urlunparse((val, parsed_origin_url.netloc, parsed_origin_url.path,
                                parsed_origin_url.params, parsed_origin_url.query, parsed_origin_url.fragment))

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, val):
        """
        Update host
        Should update:
            1. url
            2. host
            3. root_url

        :type val : str
        """
        parsed_origin_url = urlparse(self.url)
        """:type : ParseResult"""

        #update url: host & root_url will also be updated here
        self.url = urlunparse((parsed_origin_url.scheme, val, parsed_origin_url.path,
                                parsed_origin_url.params, parsed_origin_url.query, parsed_origin_url.fragment))

    @property
    def root_url(self):
        return self._root_url

    @root_url.setter
    def root_url(self, val):
        """
        Update root_url
        Should update:
            1. url
            2. scheme
            3. host
            4. root_url

        :type val : str
        """
        parsed_url = urlparse(val)
        parsed_origin_url = urlparse(self.url)
        """
        :type parsed_url : ParseResult
        :type parsed_origin_url : ParseResult
        """

        #update url: scheme & host will be updated here
        self.url = urlunparse((parsed_url.scheme, parsed_url.netloc,
                               parsed_origin_url.path, parsed_origin_url.params,
                               parsed_origin_url.query, parsed_origin_url.fragment))




