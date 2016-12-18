from widget_types import DataSink
from urlparse import urlparse

import paramiko


class RunRemoteCommandSink(DataSink):
    """
    Read data in from stdin
    """

    @classmethod
    def supportedProtocols(cls):
        return {"exec-ssh"}

    def __init__(self, uri):
        self._uri = uri

    def run(self):
        uri = urlparse(self._uri)
        client = paramiko.client.SSHClient()
        client.load_system_host_keys()
        client.connect(uri.hostname, uri.port, uri.username, uri.password)

        cmd_str = ''.join(self._source.stream)
        client.exec_command(cmd_str)