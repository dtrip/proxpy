#!/usr/bin/env python3
import socket
import logging

log = logging.getLogger()

class Forward(object):
    def __init__(self):
        self.fwd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.fwd.connect((host, int(port)))
            return self.fwd
        except Exception as e:
            log.exception(e)
            return False



