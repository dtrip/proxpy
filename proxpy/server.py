#!/usr/bin/env python3
import select
import sys
import fcntl
import os
import logging
import socket
import ssl
import socks
import threading
# import time
import urllib.request
from proxpy import Forward
from proxpy import Parser

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
        log.debug("---- New Proxy thread: %s" % (str(addr)))
        req = c.recv(self.args['receive'])
        
        p = self.proxies.getRandom()
        # print(p)
        
        log.debug("Connecting to proxy: %s %s:%s" % (p['type'], p['host'], p['port']))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(60)
            # s.connect(('23.19.32.110',3128))
            s.connect((p['host'], int(p['port'])))

            log.debug("Request:\n%s" % (req))

            meth = Parser.Parser.getHttpMethod(req)

            if meth.upper() == 'CONNECT':
                # reqPath = Parser.Parser.getReqPath(req)

                # abs = Parser.Parser.checkReqestAbsolute(reqPath)
                # log.debug(abs)
                # if not absr
                    # req = Parser.Parser.addHttpsToReqPath(req)

                log.debug("Sending connect to proxy: \n %s" % (req))
                s.send(req)
                req = s.recv(4096)
                # req = self.recFrom(s)
                log.debug(req)

                log.debug("forwarding response to client")
                c.send(req)
                # req = self.recFrom(c)
                req = c.recv(4096)

                # log.debug("Closing client socket and accepting a new one")
                # c.close()
                # c, addr = self.srv.accept()
                # print(data)
                # req = c.recv(self.args['receive'])

                # req = req.decode('utf-16')
                log.debug("Next Request: %s" % (req))

                # req = req.encode()
                # if not abs:
                    # req = Parser.Parser.addHttpsToReqPath(req)





            s.send(req)

            data = self.recFrom(s)
            c.sendall(data)
            # c.sendall(data)

            # while True:
            #     try:
            #         data = s.recv(self.args['receive'])
            #         log.debug("FInal data rec: %s" % (data))
            #         if len(data) > 0:
            #             c.send(data)
            #         else:
            #             break
            #     except socket.timeout:
            #         log.warning("HTTP Timeout")

            s.close()
            c.close()
        except Exception as e:
            log.exception(str(e))
            if s:
                log.debug("Closing socket to proxy server")
                s.close()
            if c:
                log.debug("Closing socket to client")
                c.close()
        except ConnectionRefusedError as cre:
            log.error(cre)
            

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

    def recFrom(self, conn):
        chunks = []
        bytes_recd = 0
        # buffer = bytearray()
        conn.settimeout(60)

        try:

            while True:
                chunk = conn.recv(4096)

                if len(chunk) > 0:
                    chunks.append(chunk)
                    bytes_recd = bytes_recd + len(chunk)
                else:
                    break

        except Exception as e:
            log.debug(e)

        buffer = b''.join(chunks)

        log.debug("Total Data Received: %s" % (buffer))
        return buffer

    def recFromTo(self, cFrom, cTo):
        cFrom.settimeout(60)

        try:
            while True:
                data = cFrom.recv(self.args['receive'])
                log.debug("Data Transmitted: %s" % (data))

                if len(data) > 0:
                    cTo.send(data)
                else:
                    break
        except Exception as e:
            log.debug(e)

        return True

    def hexDump(src, length=16):
        result = []
        digists = 4 if isinstance(src, unicode) else 2
        for i in range(len(src), length):
            s = src[i:i+length]
            hexa = b' '.join(['%0*X' % (digits, ord(x)) for x in s])
            text = b''.join([x if 0x20  <= ord(x) < 0x7F else b'.' for x in s])
            result.append(b"%04X %-*s %s" % (i, length*(digits + 1), hexa, text))
