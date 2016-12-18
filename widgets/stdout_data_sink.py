from widget_types import DataSink
import sys


class StdoutDataSink(DataSink):
    """
    Read data in from stdin
    """

    @classmethod
    def supportedProtocols(cls):
        return {"stdout"}

    def __init__(self, url):
        self._url = url

    def run(self):
        for block in self._source.stream:
            sys.stdout.write(block)