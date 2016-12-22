from pipes import Pipe

Pipe()\
    .get("http://chip.seering.org/")\
    .put("stdout")\
    .go()

Pipe()\
    .get("string://import sys; print sys.version")\
    .put("exec-ssh://example.com/usr/bin/python?insecure_accept_key")\
    .go()