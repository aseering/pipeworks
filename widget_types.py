from registrar import Registrar

class Metadata(object):
    """
    Metadata associated with a stream
    describing the format of the data contained within the stream
    """
    # TODO: Track state here
    pass

class DataSource(object):
    """
    Data source -- pulls data into the pipeworks
    """

    # Automatically register child classes
    class _AutoRegister(type):
        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)
            Registrar.registerSource(cls)
    __metaclass__ = _AutoRegister

    @classmethod
    def supportedProtocols(cls):
        """
        :return: URI protocols supported by this source
        :rtype: set
        """
        return {}

    @property
    def stream(self):
        """
        :return: Stream of blocks of data from this source
        :rtype: iterator[str]
        """
        raise NotImplementedError

    @property
    def streamMetadata(self):
        """
        :return: Information describing the contents of `stream`
        :rtype: Metadata
        """
        return Metadata()


class DataPipe(object):
    """
    Moves data from one stage in the pipeworks to the next
    """

    # Automatically register child classes
    class _AutoRegister(type):
        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)
            Registrar.registerPipe(cls)
    __metaclass__ = _AutoRegister

    @classmethod
    def supportedProtocols(cls):
        """
        :return: URI protocols supported by this source
        :rtype: set
        """
        return {}

    def setSource(self, source):
        """
        :param source: DataSource (or DataPipe) to read data from
        """
        self._source = source

    @property
    def stream(self):
        """
        :return: Stream of blocks of data as processed by this pipe
        :rtype: iterator[str]
        """
        assert self._source, "Must specify a source first"
        return self._source.stream()

    @property
    def streamMetadata(self):
        """
        :return: Information describing the contents of `stream`
        """
        assert self._source, "Must specify a source first"
        return self._source.streamMetadata()


class DataSink(object):
    """
    Consumes data at one end of the pipeworks
    """

    # Automatically register child classes
    class _AutoRegister(type):
        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)
            Registrar.registerSink(cls)
    __metaclass__ = _AutoRegister

    @classmethod
    def supportedProtocols(cls):
        """
        :return: URI protocols supported by this source
        :rtype: set
        """
        return {}

    def setSource(self, source):
        """
        :param source: DataSource (or DataPipe) to read data from
        """
        self._source = source

    def streamMetadata(self):
        """
        :return: Information describing the contents of `stream`
        """
        assert self._source, "Must specify a source first"
        return self._source.streamMetadata()

    def run(self):
        """
        :return: Consume all of the source data
        """
        raise NotImplementedError
