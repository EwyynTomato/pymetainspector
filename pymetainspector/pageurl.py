try: #Python 3 import
    from urllib.parse import urlparse, urlunparse
except ImportError: #Fallback to Python 2
    from urlparse import urlparse, urlunparse

class PageURL(object):
    """
    Result page object containing information from inspected url/html
    """
    def __init__(self):
        self._url = None
        self._scheme = None
        self._host = None
        self._root_url = None

    def __repr__(self):
        return "<%s : %s>" % (self.__class__.__name__, self.__dict__)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, val):
        """
        Parse url and set the url info into Page's object instances

        :type val : str
        """
        parsed_absolute_url = urlparse(self.to_absolute_url(val))

        #- Set: url, scheme, host, root_url
        self._scheme = parsed_absolute_url.scheme
        self._host = parsed_absolute_url.hostname
        self._root_url = urlunparse((parsed_absolute_url.scheme, parsed_absolute_url.netloc, "/", '', '', ''))
        normalized_path = parsed_absolute_url.path if parsed_absolute_url.path else "/"
        self._url = urlunparse((self._scheme, self.host, normalized_path,
                                parsed_absolute_url.params, parsed_absolute_url.query, parsed_absolute_url.fragment))


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


    @staticmethod
    def is_absolute_url(url):
        return bool(urlparse(url).scheme) and bool(urlparse(url).netloc)

    @staticmethod
    def add_http_scheme_if_scheme_missing(url):
        if not urlparse(url).scheme:
            url = "http:%s%s" % ("" if url.startswith("//") else "//", url) # Should use http:// scheme by default
        return url

    def to_absolute_url(self, url):
        if self.is_absolute_url(url):
            return url
        else:
            url = self.add_http_scheme_if_scheme_missing(url)
            parsed_url = urlparse(url)
            """:type parsed_url : ParseResult"""

            hostname = parsed_url.hostname or self.host

            return urlunparse((parsed_url.scheme, hostname, parsed_url.path,
                               parsed_url.params, parsed_url.query, parsed_url.fragment))

