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

try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser  # noqa: F401


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
        self.q = None

        self.s = None

    # set threads event handler to wait for socket connection before making request
    def setThreadEvent(self, e):
        self.e = e
        return True

    # set queue for returning data
    def setQueue(self, q):
        self.q = q
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
        res = None

        try:
            log.debug("adding thread %s to pool" % self.getName())
            if (self.s is None):
                self.createSocket(self.host, int(self.port))

            res = self.makeRequest(self.domain, self.url)
        except Exception as e:
            log.exception(e.message)
        finally:
            log.debug("Closing thread: %s" % self.getName())
            self.pool.release()
            # thread

        return res

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
        evSet = self.e.wait()  # noqa: F841
        # log.debug("Generating raw http request")
        self.s.connect((host, port))
        req = self.rawHttpReq(host, self.url)

        self.s.sendall(req)

        headers = []
        body = []
        p = HttpParser()

        while True:
            data = self.s.recv(2048)

            if not data:
                break

            rlen = len(data)
            nparsed = p.execute(data, rlen)
            assert nparsed == rlen

            if p.is_headers_complete():
                headers = p.get_headers()
                # log.debug(p.get_headers())
            if p.is_partial_body():
                body.append(p.recv_body())

            if p.is_message_complete():
                break

        self.s.close()
        self.q.put({'status': p.get_status_code(), 'headers': headers, 'body': body})

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
