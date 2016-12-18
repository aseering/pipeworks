from pipes import Pipe

Pipe()\
    .get("http://chip.seering.org/")\
    .put("stdout")\
    .go()

Pipe()\
    .get("string://hostname")\
    .put("exec-ssh://")