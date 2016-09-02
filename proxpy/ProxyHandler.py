#!/usr/bin/env python
from __future__ import division, print_function
import logging
import sys
import socket
import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpclient

import parser

log = logging.getLogger()

__all__ = ['ProxyHandler']

class ProxyHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST', 'CONNECT']

    @tornado.web.asynchronous
    def get(self):
            def handle_response(response):
                log.debug("response Handle")
                if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
                    self.set_status(500)
                    self.write('Internal server error:\n' + str(response.error))
                    self.finish()
                else:
                    self.set_status(response.code)
                    for header in ('Date', 'Cache-Control', 'Server', 'Content-Type', 'Location'):
                        v = response.headers.get(header)
                        if v:
                            self.set_header(header, v)

                    if response.body:
                        self.write(response.body)

                    self.finish()

            req = tornado.httpclient.HTTPRequest(
                    url=self.request.uri,
                    method=self.request.method,
                    body=self.request.body,
                    headers=self.request.headers,
                    follow_redirects=False,
                    allow_nonstandard_methods=True
            )

            client = tornado.httpclient.AsyncHTTPClient()

            try:
                client.fetch(req, handle_response)
            except tornado.httpclient.HTTPError as e:
                if hasattr(e, 'response') and e.response:
                    self.handle_response(e.response)
                else:
                    self.set_status(500)
                    self.write('Internal Server Error:\n' + str(e.message))
                    self.finish()

    @tornado.web.asynchronous
    def post(self):
        return self.get()

    
    @tornado.web.asynchronous
    def connect(self):
        log.debug("Start CONNECT to %s" % (self.request.uri))
        host, port = self.request.uri.split(':')
        client = self.request.connection.stream

        def read_from_client(data):
            upstream.write(data)

        def read_from_upstream(data):
            client.write(data)

        def client_close(data=None):
            if upstream.closed():
                return

            if data:
                upstream.write(data)

            upstream.close()

        def upstream_close(data=None):
            if client.closed():
                return

            if data:
                client.write(data)
            
            client.close()

        def start_tunnel():
            log.debug("Connect tunnel established to %s" % (self.request.uri))
            client.read_until_close(client_close, read_from_client)
            upstream.read_until_close(upstream_close, read_from_upstream)
            client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

        def on_proxy_response(data=None):
            if data:
                first_line = data.splitlines()[0]
                http_v, swtatus, text = first_line.split(None, 2)
                if int(status) ==  200:
                    log.debug("connect to upstream proxy %s" % (proxy))
                    start_tunnel()
                    return

            self.set_status(500)
            self.finish()


        def start_proxy_tunnel():
            upstream.write("CONNECT %s HTTP/1.1\r\n" % (self.request.uri))
            upstream.write("Host: %s\r\n" % (self.request.uri))
            upstream.write("Proxy-Connection: Keep-Alive\r\n\r\n")
            upstream.read_until("\r\n\r\n", on_proxy_response)


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        upstream = tornado.iostream.IOStream(s)
        # upstream.connect((host, int(port)), start_tunnel)
        proxy = get_proxy(self.request.uri)

        if proxy:
            proxy_host, proxy_port = parser.parse_proxy(proxy)
            upstream.connect((proxy_host, proxy_port), start_proxy_tunnel)

