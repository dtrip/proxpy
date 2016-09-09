#!/usr/bin/env python3
import logging
import socket
import select
import threading

log = logging.getLogger()


class connection(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        threading.Thread.__init__(self)


    def run(self):

        try:
            while True:

                r, w, e = select.select(self.input_list, [], [])

                data = conn.recv(1024)

                if data == "":
                    log.debug("socket closed remotely")
                    break
                log.debug("Received data %r" % data)

                conn.sendall(data)
                log.debug("sent data")


        except:
            log.exception("Error handling request")
        finally:
            log.debug("Closing socket")
            conn.close()
