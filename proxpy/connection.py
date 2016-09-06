#!/usr/bin/env python3
import sys
import logging
import socket
import fcntl
import os
import select

log = logging.getLogger()

class connection(object):

    MAX_BUFFER_SIZE = 1024

    def __init__(self, proxyserver, sock, srvaddr, args):
        self.args = args
        self.proxyserver = proxyserver
        self.srvaddr = srvaddr

        self.clisock, self.cliaddr = sock.accept()
        self.clisock.setblocking(0)

        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setblocking(0)
        
        self.buffers = { self.clisock:bytes(), self.srvsock:bytes() }

        self.connected = False

        self.proxyserver.registerSocket(self.clisock, self)
        self.proxyserver.registerSocket(self.srvsock, self)
        self.proxyserver.activateRead(self.clisock)
        self.proxyserver.activateRead(self.srvsock)


    def other(self, s):
        if socket == self.clisock:
            return self.srvsock
        else:
            return self.clisock

    def connect(self):
        # log.debug("Making connection_ex to proxy address %s - Connections: %d" % (str(self.addr)))
        self.srvsock.connect_ex(self.srvaddr)

    def readfrom(self, s):

        if s == self.srvsock and not self.connected:
            self.proxyserver.connection_count += 1
            log.info("opened connection from %s, connection count now %d" % (str(self.cliaddr), self.proxyserver.connection_count))
            self.connected = True
            return

        capacity = connection.MAX_BUFFER_SIZE - len(self.buffers[s])

        try:
            data = s.recv(capacity)
        except Exception as e:
            data = ""
            log.warning(e.message)

        if len(data) == 0:
            self.close()
            return

        self.buffers[s] += data
        self.proxyserver.activateWrite(self.other(s))

        capacity -= len(data)

        if capacity <= 0:
            self.proxyserver.deactivateRead(s)

    def writeto(self, s):
        buf = self.buffers[self.other(s)]

        written = s.send(buf)

        buf = buf[written:]

        self.buffers[self.other(s)] = buf

        if len(buf) == 0:
            self.proxyserver.deactivateWrite(s)

        if written:
            self.proxyserver.activateRead(self.other(s))

    def close(self):
        for sock in [self.clisock, self.srvsock]:
            if sock:
                self.proxyserver.deactivateRead(sock)
                self.proxyserver.deactivateWrite(sock)

                sock.close()

                self.proxyserver.unregisterSocket(sock, self)

        self.proxyserver.connection_count -= 1
        log.info("Connection closed (%d)" % (self.proxyserver.connection_count))
