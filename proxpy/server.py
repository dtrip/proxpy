#!/usr/bin/env python3
import select
import sys
import fcntl
import os
import logging
import socket
import threading
from proxpy import Forward

log = logging.getLogger()


class server(object):
    def __init__(self, args):
        self.args = args
        self.address = (self.args['interface'], self.args['port'])
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv.bind(self.address)
        self.srv.listen(200)

        self.input_list = []
        self.channel = {}


    def run(self):
        loop = 0
        self.input_list.append(self.srv)

        while True:

            r, w, e = select.select(self.input_list, [], [])

            loop += 1

            for self.s in r:

                if self.s is self.srv:
                    self.on_accept()
                    break
                self.data = self.s.recv(self.args['receive'])

                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()


    def on_accept(self):
        fwd = Forward.Forward().start('127.0.0.1', 9050)
        clientsock, clientaddr = self.srv.accept()
        clientsock.settimeout(60)
        
        # t = threading.Thread(target = self.listenToClient, args = (clientsock, clientaddr))
        # fwd.setDaemon(True)
        # fwd.start()

        if fwd:
            log.debug("%s has connected" % (str(clientaddr)))
            self.input_list.append(clientsock)
            self.input_list.append(fwd)
            self.channel[clientsock] = fwd
            self.channel[fwd] = clientsock
        else:
            log.warning("Can't establish connection with remote server. Closing client side connection: %s" % (clientaddr))
            clientsock.close()

    def listenToClient(self, c, addr):
       size = 1024

       while True:
            try:
               data = c.recv(size)

               if data:
                   response = data
                   c.send(response)
               else:
                    log.error("client disconnected")
                    raise error('client disconnected')
            except:
                c.close()
                # log.exception(e)
                return False
    
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
