#!/usr/bin/env python3
import socket
import logging

log = logging.getLogger()

class Forward(object):
    def __init__(self):
        self.fwd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):

        assert len(host) > 0

        try:
            if type(port) is not int:
                port = int(port)

            log.debug("Connecting to %s:%d" % (host, port))

            self.fwd.connect((host, port))
            return self.fwd
        except Exception as e:
            log.exception(e)
            raise
            return False



