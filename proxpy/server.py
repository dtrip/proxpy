#!/usr/bin/env python
from __future__ import division, print_function
import sys
import threading
import socket
import signal
# import receiver


class server():
    def __init__(self, p):

        self.proxpy = p
        # self.s = socket

        signal.signal(signal.SIGINT, self.shutdown)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try: 
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.proxpy.args['interface'], self.proxpy.args['port']))
        self.s.listen(int(self.proxpy.args['backlog']))
        self.clients = {}
        # self.__srvLoop()
        # except socket.error as e:

        # self.proxpy.log.error("Unable to open socket: %s", (str(e)))
        # raise

    def listenClients(self):
        while True:
            try:
                (conn, addr) = self.s.accept()
                data = conn.recv(self.proxpy.args['receive'])
                print(data)
                d = threading.Thread(target=self.proxy_thread, args=(conn, data, addr))
                d.setDaemon(True)
                d.start()
            except socket.error as e:
                self.proxpy.log.error(e)

        self.shutdown(0, 0)

    def proxy_thread(self, conn, data, addr):
        self.proxpy.log.debug("Addr: %s" % (addr))
        request = conn.recv(self.proxpy.args['receive'])

        first_line = data.split('\n')[0]

        print("'" + first_line.decode() + "'")
        print(len(first_line))
        if (len(first_line) > 0):
            url = first_line.split(' ')[1]
        else:
            url = ""

        http_pos = url.find("://")

        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos + 3):]

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
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
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
            # self.proxpy.log.error(e)
            print(str(e))

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
        sys.exit(0)
