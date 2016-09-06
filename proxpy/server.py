#!/usr/bin/env python3
import select
import sys
import fcntl
import os
import logging
import socket
from proxpy import connection, Forward

log = logging.getLogger()


class server(object):
    def __init__(self, args):
        self.args = args
        self.address = (self.args['interface'], self.args['port'])
        self.srvaddr = ('127.0.0.1', 9050)
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv.bind(self.address)
        self.srv.listen(200)
        self.connections = {}
        self.readsockets = []
        self.writesockets = []


        self.input_list = []
        self.channel = {}

        self.allsockets = [self.srv]
        self.connection_count = 0

    def run(self):
        loop = 0
        self.input_list.append(self.srv)

        while True:
            # r, w, e = select.select(
            #         # [self.srv]+self.readsockets,
            #         self.writesockets,
            #         self.allsockets,
            #         60
            # )

            r, w, e = select.select(self.input_list, [], [])

            loop += 1

            for self.s in r:

                if self.s is self.srv:
                    self.on_accept()
                    break
                    # self.open()C
                # else:
                    # if s in self.connections:
                        # self.connections[s].readfrom(s)
                self.data = self.s.recv(self.args['receive'])

                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()

            # for s in w:
                # if s in self.connections:
                    # self.connections[s].writeto(s)

            # handle errors (close connections)
            # for s in e:
                # log.error("Socket error closing connection")
                # if s in self.connections:
                    # self.connections[s].close()

        # self.srv.close()
        # self.srv = None

    def on_accept(self):
        fwd = Forward.Forward().start('127.0.0.1', '9050')
        clientsock, clientaddr = self.srv.accept()

        if fwd:
            log.debug("%s has connected" % (str(clientaddr)))
            self.input_list.append(clientsock)
            self.input_list.append(fwd)
            self.channel[clientsock] = fwd
            self.channel[fwd] = clientsock
        else:
            log.warning("Can't establish connection with remote server. Closing client side connection: %s" % (clientaddr))
            clientsock.close()
    
    def on_close(self):
        log.info("%s has disconnected" % (str(self.s.getpeername())))
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]

        self.channel[out].close()

        self.channel[self.s].close()

        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data

        # log.info(data)
        self.channel[self.s].send(data)

    def activateRead(self, sock):
        if not sock in self.readsockets:
            log.debug("Activating read socket for %s" % (str(sock)))
            self.readsockets.append(sock)

    def deactivateRead(self, sock):
        if sock in self.readsockets:
            log.debug("removing read socket for %s" % (str(sock)))
            self.readsockets.remove(sock)

    def activateWrite(self, sock):
        if not sock in self.writesockets:
            log.debug("activating write socket for %s" % (str(sock)))
            self.writesockets.append(sock)

    def deactivateWrite(self, sock):
        if sock in self.writesockets:
            log.debug("removing write socket for %s" % (str(sock)))
            self.writesockets.remove(sock)

    def registerSocket(self, sock, conn):
        log.debug("Registering socket %s at connection %s" % (str(sock), str(conn)))
        self.connections[sock] = conn
        self.allsockets.append(sock)

    def unregisterSocket(self, sock, conn):
        log.debug("Removing socket %s at connection %s" % (str(sock), str(conn)))
        del self.connections[sock]
        self.allsockets.remove(sock)

    def open(self):
        log.debug("Opening new connection %s" % (str(self.address)))
        conn = connection.connection(self, self.srv, self.srvaddr, self.args)
        conn.connect()

