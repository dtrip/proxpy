#!/usr/bin/env python

from __future__ import division, print_function

import socket
import os
import thread

class server(object):
    def __init__(self, host, port):
        try: 
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((host, port))
            self.listen(BACKLOG)
        except socket.error, (value, msg):
            if s:
                s.close()
            print("Unable to open socket: %s" % (msg))
            raise

        self.__srvLoop()

    def __srvLoop(self):
        while True:
            try:
                conn, clientAdr = s.accept()

                thread.start_new_thread(proxy_thread, (conn, client_addr))
            except valueError as e:
                pass
            except Exception as e:
                pass
            finally:
                s.close()

        return True


    def proxyThread(self, conn, client_addr):
        req = conn.recv(MAX_DATA_RECV)

        fl = req.split('n')[0]

        url = fl.split(' ')[1]

        if (self.args.debug):
            print("%s\n%s\n" % (fl, url))

        http_pos = url.find("://")

        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos+3):]

        port_pos = temp.find(":")

        webserver_pos = temp.find("/")

        if (webserver_pos == -1):
            webserver_pos = len(temp)

        if (port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver_pos = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        print("Connect to: %s:%d" % (webserver, port))

        try:
            # create socket and and make request
        except socket.error, (value, msg):
            if s:
                s.close()
            
            if conn:
                conn.close()

            print("Runtime Error: %s" % (msg));
            

            

