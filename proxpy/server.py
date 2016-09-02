#!/usr/bin/env python
from __future__ import division, print_function
import sys
# import threading
import socket
import ProxyHandler
# import signal
# import receiver


import socket
import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpclient


__all__ = ['run']

class server(object):
    def __init__(self):
        # self.run()
        self.app = tornado.web.Application([
            (r'/', ProxyHandler),
        ])

    def run(self, port=8080, start_ioloop=True):

        app = tornado.web.Application([
                (r'.*', ProxyHandler)
            ])

        app.listen(8080)

        # httpServer = tornado.httpserver.HTTPServer(self.app)
        # httpServer.listen(8080)

        ioloop = tornado.ioloop.IOLoop.instance()

        if start_ioloop:
            ioloop.start()

