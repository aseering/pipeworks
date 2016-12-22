
class Registrar(object):
    """
    Register data implementations
    """

    _SOURCE_HANDLERS = {}
    _PIPE_HANDLERS = {}
    _SINK_HANDLERS = {}

    @classmethod
    def registerSource(cls, src):
        for proto in src.supportedProtocols():
            cls._SOURCE_HANDLERS[proto] = src

    @classmethod
    def registerSink(cls, snk):
        for proto in snk.supportedProtocols():
            cls._SINK_HANDLERS[proto] = snk

    @classmethod
    def registerPipe(cls, pipe):
        for proto in pipe.supportedProtocols():
            cls._PIPE_HANDLERS[proto] = pipe


    @classmethod
    def getSource(cls, srcProto):
        return cls._SOURCE_HANDLERS[srcProto]

    @classmethod
    def getSink(cls, snkProto):
        return cls._SINK_HANDLERS[snkProto]

    @classmethod
    def getPipe(cls, pipeProto):
        return cls._PIPE_HANDLERS[pipeProto]

