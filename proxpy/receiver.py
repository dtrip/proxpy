#!/usr/bin/env python

from __future__ import division, print_function

import threading

class receiver(threading.Thread):

    def __init__(self, p, conn, client_addr):
        threading.Thread.__init__(self)
        self.proxpy = p
        self.__recvThread(conn, client_addr)

    def __recvThread(self, conn, client_addr):
        self.proxpy.log.debug("Processing thread")
        print(conn)
        print(client_addr)
        request = conn.recv(4096)

        # help(request)
        # self.proxpy.log.debug(str(request))

        first_line = request.split('\n')[0]
        self.proxpy.log.debug("First Line: %s", (first_line))
        url = first_line.split(' ')[1]

        self.proxpy.log.debug("%s\n%s\n", (fl, url))

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

        self.proxpy.log.debug("Connect to: %s:%d", (webserver, port))

        try:
            pass
            # create socket and and make request
        except socket.error as e:
            if self.s:
		self.s.close()
            
            if conn:
                conn.close()

            self.proxpy.log.error("Runtime Error: %s", (msg));


