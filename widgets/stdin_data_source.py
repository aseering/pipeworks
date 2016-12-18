from widget_types import DataSource
import sys

DEFAULT_CHUNK_SZ = 4 * 1024 * 1024


class StdinDataSource(DataSource):
    """
    Read data in from stdin
    """

    @classmethod
    def supportedProtocols(cls):
        return {"stdin"}

    def __init__(self, url):
        self._url = url

    @property
    def stream(self):
        while True:
            chunk = sys.stdin.read(DEFAULT_CHUNK_SZ)
            if not chunk:
                break
            yield chunk