#!/usr/bin/env python3
import select
import sys
import fcntl
import os
import logging
import socket
import socks
import threading
# import time
import urllib.request
from proxpy import Forward

log = logging.getLogger()


class server(object):
    def __init__(self, args, proxies):
        self.args = args

        self.proxies = proxies

        self.default_socket = socket.socket

        self.address = (self.args['interface'], self.args['port'])
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv.bind(self.address)
        self.srv.listen(200)

        self.__clients = {}

        self.threads = []
        self.input_list = []
        self.channel = {}


    def run(self):
        while True:
            c, addr = self.srv.accept()
            t = threading.Thread(name='client', target=self.proxyThread, args=(c, addr))
            t.setDaemon(True)
            t.start()

    def proxyThread(self, c, addr):
        req = c.recv(self.args['receive'])
        
        p = self.proxies.getRandom()
        # print(p)
        
        log.debug("Connecting to proxy: %s %s:%s" % (p['type'], p['host'], p['port']))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(60)
            # s.connect(('23.19.32.110',3128))
            s.connect((p['host'], int(p['port'])))
            s.sendall(req)

            while True:
                data = s.recv(self.args['receive'])
                if len(data) > 0:
                    c.send(data)
                else:
                    break

            s.close()
            c.close()
        except Exception as e:
            if s:
                s.close()
            if c:
                c.close()
            log.exception(e)

    def on_accept(self):
        clientsock, clientaddr = self.srv.accept()
        clientsock.settimeout(60)
        
        log.debug("staring thread for client: %s %s" % (clientsock, clientaddr))
        t = threading.Thread(target = self.listenToClient, args = (clientsock, clientaddr))
        t.start()

        self.threads.append(t)

    def listenToClient(self, c, addr):
        size = 1024

        log.debug("listen to client: %s %s" % (c, addr))

        fwd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fwd.connect(('23.19.32.110', int(3128)))
        # fwd = Forward.Forward().start()
        # c, addr = self.srv.accept()
        # c.settimeout(60)

        if fwd:
            log.debug("%s has connected " % (str(addr)))

            self.input_list.append(c)
            self.input_list.append(fwd)
            self.channel[c] = fwd
            self.channel[fwd] = c
        else:
            log.warning("Can't establish connection with remote server. Closing client side connection: %s" % (clientaddr))
            c.close()

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
