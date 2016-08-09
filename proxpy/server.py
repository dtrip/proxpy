#!/usr/bin/env python

from __future__ import division, print_function

import os
import sys
# from threading import Thread
import threading
import socket
import signal
# import receiver

class server(object):
    def __init__(self, p):

        self.proxpy = p
        # self.s = socket

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.proxpy.args['interface'], self.proxpy.args['port']))
            self.s.listen(int(self.proxpy.args['backlog']))
            self.clients = {}
            self.__srvLoop()
        except socket.error as e:
            # pass
            # if self.s:
                # self.s.close()

            self.proxpy.log.error("Unable to open socket: %s", (str(e)))
            raise


    def __srvLoop(self):
        while True:
            (conn, addr) = self.s.accept()
            d = threading.Thread(target=self.proxy_thread, args=(conn, addr))
            d.setDaemon(True)
            d.start()
        self.shutdown(0,0)
        

    def proxy_thread(self, conn, addr):
        request = conn.recv(self.proxpy.args['receive'])

        first_line = request.split('\n')[0]
        url = first_line.split(' ')[1]

        http_pos = url.find("://")

        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos+3):]

        port_pos = temp.find(":")

        webserver_pos = temp.find("/")

        if (webserver_pos == -1):
            webserver_pos = len(temp)

        webserver = ""
        port = -1

        if (port_pos == -1 or webserver < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]


        try:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((webserver, port))
            s.sendall(request)

            while 1:
                data = s.recv(self.proxpy.args['receive'])

                if (len(data) > 0):
                    conn.send(data)
                else:
                    break
            s.close()
            conn.close()
        except socket.error as e:
            self.proxpy.log.error(e)

            if s:
                s.close()

            if conn:
                conn.close()

    def shutdown(self, signum, frame):
        self.proxpy.log.warning("Attempting to shutdown gracefully")

        main_thread = threading.currentThread()

        for t in threading.enumerate():
            if t is main_thread:
                continue
                self.proxpy.log.error("Error joining " + t.getName())

            t.join()
            self.s.close()
        # self.s.close()
        sys.exit(0)
