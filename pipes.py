from registrar import Registrar
import widgets.import_all

from copy import deepcopy
from urlparse import urlparse
from threading import Thread

class UnknownURI(Exception):
    def __init__(self, uri):
        super(Exception, self).__init__("Unrecognized URI: '%s'" % uri)

class Pipe(object):
    class _BasicPipe(object):
        """
        Handles a linear pipeline of data processing
        """

        def __init__(self):
            self._src = None
            self._pipes = []
            self._snk = None

        def setSource(self, src):
            """
            :param DataSource src: Source to consume data from
            """
            self._src = src

        def addPipe(self, pipe):
            """
            :param DataPipe pipe: Pipe to append to the current series of pipes
            """
            self._pipes.append(pipe)

        def setSink(self, snk):
            """
            :param DataSink snk: DataSink that will consume all of the data
            """
            self._snk = snk

        def hasSink(self):
            """
            :return: True iff 'setSink()' has already been called
            """
            return self._snk is not None

        def run(self):
            """
            Consume all data in the pipe
            """
            for src, snk in zip([self._src] + self._pipes,
                                self._pipes + [self._snk]):
                snk.setSource(src)

            self._snk.run()

    def __init__(self):
        self._newPipe()
        self._targetHost = None

    def _newPipe(self):
        self._current_pipe = self._BasicPipe()
        self._pipes = {self._current_pipe}

    def _uri_scheme(self, url):
        if ':' not in url:
            return url  # Simple scheme, ie., 'stdin'
        return urlparse(url).scheme

    def get(self, uri):
        uri_scheme = self._uri_scheme(uri)
        try:
            Src = Registrar.getSource(uri_scheme)
        except KeyError:
            raise UnknownURI(uri)
        self._current_pipe.setSource(Src(uri))
        return self

    def put(self, uri):
        uri_scheme = self._uri_scheme(uri)
        try:
            Snk = Registrar.getSink(uri_scheme)
            self._current_pipe.setSink(Snk(uri))
        except KeyError:
            try:
                Pip = Registrar.getPipe(uri_scheme)
                self._current_pipe.addPipe(Pip(uri))
            except KeyError:
                raise UnknownURI(uri)
        return self

    def go(self):
        if not self._current_pipe.hasSink():
            # Output to our own stdout by default
            self.put("stdout")

        if self._targetHost == None:
            return self._local_go()

        remote_pipe = deepcopy(self)
        remote_pipe._targetHost = None
        

    def _local_go(self):
        threads = [Thread(target=lambda: pipe.run()) for pipe in self._pipes]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self
