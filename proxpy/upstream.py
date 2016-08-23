#!/usr/bin/env python
from __future__ import division, print_function
# import urllib2
import socks
import threading
# import types
# import numbers
import logging
# from sockshandler import SocksiPyHandler       
log = logging.getLogger()


class upstream(threading.Thread):

    def __init__(self, pool, host, port, domain, url):
        threading.Thread.__init__(self)

        self.pool = pool
        self.host = host
        self.port = port
        self.domain = domain
        self.url = url

        # if p is not None:
        # self.proxpy = p
        # self.opener = None
        # self.socksHandler = None
        self.s = None

    def createSocket(self, host, port):
        self.s = socks.socksocket()

        assert host is not None
        assert port is not None and type(port) is int and port > 0 and port <= 65535

        log.debug("connecting to socks proxy: %s:%d" % (host, port))
        # socks proxy type can be socks.SOCKS5, socks.SOCKS4, socks.HTTP
        try:
            self.s.set_proxy(socks.SOCKS5, host, port, True)
        except self.s.ProxyConnectionError as e:
            log.exception(e.message)
            raise
        except self.s.GeneralProxyError as e:
            log.exception(e.message)
            raise
        except Exception as e:
            log.exception(e.message)
            raise

        return True

    def run(self):
        # limiter = threading.BoundSemaphore(
        log.debug("runing")

        self.pool.acquire()

        try:
            log.debug("adding thread %s to pool" % self.getName())
            if (self.s is None):
                self.createSocket(self.host, int(self.port))

            self.makeRequest(self.domain, self.url)

        finally:
            log.debug("Closing thread: %s" % self.getName())
            self.pool.release()
            # thread

    def connectHost(self, url, port=80): 
        assert url is not None

        log.debug("Connecting to host %s:%d" % (url, port))

        # return self.opener.open(url)
        try:
            return self.s.connect((url, port))
        except self.s.ProxyConnectionError as e:
            log.warn(e.message)
            raise
        except self.s.GeneralProxyError as e:
            log.warn(e.message)
            raise
        except Exception as e:
            log.exception(e.message)
            raise
        return False

    def makeRequest(self, host, url="/"):
        assert self.s is not None and type(self.s) is socks

        req = self.rawHttpReq(host)

        self.s.sendall(req)
        status = self.s.recv(2048)

        log.debug("Status: %s" % (status))
        return True

    def rawHttpReq(self, host, url="/", userAgent="Proxpy", acpt="*/*"):

        assert host is not None

        log.debug("Building request for: %s%s" % (host, url))

        req = "GET %s HTTP/1.1\r\n" % (url)
        req += "Host: %s\r\n" % (host)
        req += "User-Agent: %s\r\n" % (userAgent)
        req += "Accept: %s\r\n" % (acpt)
        req += "\r\n"

        self.proxpy.log.debug(req)
        return req.encode()
