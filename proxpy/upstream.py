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

    def __init__(self, pool, type, host, port, domain, url, timeout=10):
        threading.Thread.__init__(self)

        if (type.lower() == 'http'):
            self.type = socks.HTTP
        elif (type.lower() == 'socks4'):
            self.type = socks.SOCKS4
        else: 
            self.type = socks.SOCKS5

        self.pool = pool
        self.host = host
        self.port = port
        self.domain = domain
        self.url = url
        self.timeout = timeout
        self.e = None

        # if p is not None:
        # self.proxpy = p
        # self.opener = None
        # self.socksHandler = None
        self.s = None

    def setThreadEvent(self, e):
        self.e = e
        return True

    def createSocket(self, host, port):
        self.s = socks.socksocket()

        assert host is not None
        assert port is not None and type(port) is int and port > 0 and port <= 65535

        log.debug("connecting to %s proxy: %s:%d" % (self.type, host, port))
        # socks proxy type can be socks.SOCKS5, socks.SOCKS4, socks.HTTP
        try:
            self.s.set_proxy(self.type, host, port, True)
            # log.debug("Setting thread event")
            self.e.set()

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
        assert self.e is not None

        self.pool.acquire()

        try:
            log.debug("adding thread %s to pool" % self.getName())
            if (self.s is None):
                self.createSocket(self.host, int(self.port))

            self.makeRequest(self.domain, self.url)
        except Exception as e:
            log.exception(e.message)
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
        finally:
            log.debug("Connected")
        return False

    def makeRequest(self, host, url="/", port=80):
        assert self.e is not None
        evSet = self.e.wait()
        # log.debug("Generating raw http request")
        self.s.connect((host, port))
        req = self.rawHttpReq(host, self.url)

        self.s.sendall(req)
        status = self.s.recv(2048)

        log.debug("Status: %s" % (status))
        return True

        # while not self.e.isSet():
        #     evSet = self.e.wait()
        #
        #     log.debug("evSet: %s%s" % (evSet, type(evSet)))
        #     if evSet:
        #         log.debug("Generating raw http request")
        #         req = self.rawHttpReq(host)
        #
        #         self.s.sendall(req)
        #         status = self.s.recv(2048)
        #
        #         log.debug("Status: %s" % (status))
        #         # return True
        #     else:
        #         log.debug("Event not yet set")

    def rawHttpReq(self, host, url="/", userAgent="Proxpy", acpt="*/*"):

        assert host is not None

        log.debug("Building request for: %s%s" % (host, url))

        req = "GET %s HTTP/1.1\r\n" % (url)
        req += "Host: %s\r\n" % (host)
        req += "User-Agent: %s\r\n" % (userAgent)
        req += "Accept: %s\r\n" % (acpt)
        req += "\r\n"

        log.debug(req)
        return req.encode()
