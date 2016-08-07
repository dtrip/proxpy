#!/usr/bin/env python

from __future__ import division, print_function

import socket
import os
import thread

class server(object):
    def __init__(self, host, port)
        try: 
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((host, port))
            self.listen(BACKLOG)
        except socket.error, (value, msg):
            if :
                s.close()
            print("Unable to open socket: %s" % (mg))
            raise

        self.__srvLoop()

    def __srvLoop(self):
        while ;;
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
