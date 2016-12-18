from widget_types import DataSource

DEFAULT_BLOCK_SZ = 10

class ConstantStringDataSource(DataSource):
    """
    Read data in from stdin
    """

    @classmethod
    def supportedProtocols(cls):
        return {"string"}

    def __init__(self, url):
        self._url = url
        assert url.startswith("string://")
        self._text = url[9:]

    @property
    def stream(self):
        # Must return a generator
        return (self._text[i : i + DEFAULT_BLOCK_SZ]
                for i in xrange(0, len(self._text), DEFAULT_BLOCK_SZ))