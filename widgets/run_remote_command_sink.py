from widget_types import DataPipe
from urlparse import urlparse, parse_qs
from threading import Thread

import paramiko

DEFAULT_BLOCK_SZ = 4 * 1024 * 1024

class RunRemoteCommandSink(DataPipe):
    """
    Read data in from stdin
    """

    @classmethod
    def supportedProtocols(cls):
        return {"exec-ssh"}

    def __init__(self, uri):
        self._uri = uri

    @property
    def stream(self):
        uri = urlparse(self._uri)
        params = parse_qs(uri.query, keep_blank_values=True)

        cmd = uri.path

        # exec-ssh://example.com/cat means "cat"
        # exec-ssh://example.com/bin/echo means "/bin/echo"
        if cmd.rfind("/") == 0:
            cmd = cmd[1:]

        client = paramiko.client.SSHClient()
        client.load_system_host_keys()

        if "insecure_accept_key" in params:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(uri.hostname, uri.port, uri.username, uri.password)

        stdin, stdout, stderr = client.exec_command(cmd)

        # Feed stdin in a separate thread so we don't deadlock on ourselves.
        # We could alternatively use 'select()', but not on Windows.
        def feed_stdin():
            for data in self._source.stream:
                stdin.write(data)
            stdin.close()

            # Work around BUG:
            # https://github.com/paramiko/paramiko/issues/322
            stdin.channel.shutdown_write()

        stdin_feeder_thread = Thread(target=feed_stdin)
        stdin_feeder_thread.daemon = True
        stdin_feeder_thread.start()

        while True:
            data = stdout.read(DEFAULT_BLOCK_SZ)
            if not data:
                return
            yield data
