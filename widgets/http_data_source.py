from widget_types import DataSource
import urllib2

DEFAULT_CHUNK_SZ = 4 * 1024 * 1024


class HttpDataSource(DataSource):
    """
    Download data over HTTP
    """

    @classmethod
    def supportedProtocols(cls):
        return {"http", "https"}

    def __init__(self, url):
        self._url = url

    @property
    def stream(self):
        f = urllib2.urlopen(self._url)

        while True:
            chunk = f.read(DEFAULT_CHUNK_SZ)
            if not chunk:
                break
            yield chunk