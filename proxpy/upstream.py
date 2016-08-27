#!/usr/bin/env python
from __future__ import division, print_function
# import urllib2
import socks
import threading
# import types
# import numbers
import logging
import base64
# from sockshandler import SocksiPyHandler       
log = logging.getLogger()

try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser  # noqa: F401


class upstream(threading.Thread):

    def __init__(self, pool, prx, domain, url, port=80, method="GET", headers=None, postdata=None, timeout=10):
        threading.Thread.__init__(self)

        self.txtType = prx['type']

        if (prx['type'].lower() == 'http'):
            self.type = socks.HTTP
        elif (prx['type'].lower() == 'socks4'):
            self.type = socks.SOCKS4
        else: 
            self.type = socks.SOCKS5

        self.pool = pool
        self.prx = prx

        self.domain = domain
        self.url = url
        self.port = port
        self.timeout = timeout
        self.e = None
        self.q = None
        self.useragent = "proxpy"

        if (headers is None):
            self.headers = {"User-Agent": "Proxpy", "Accept": "*/*"}
        else:
            self.headers = headers

        self.postdata = postdata
        self.s = None
        self.method = method

    # set threads event handler to wait for socket connection before making request
    def setThreadEvent(self, e):
        self.e = e
        return True

    # set queue for returning data
    def setQueue(self, q):
        self.q = q
        return True

    def setUserAgent(self, a):
        assert type(a) is str and a is not None
        self.useragent = a
        return True

    # connects to proxy server
    def createSocket(self, prx):
        self.s = socks.socksocket()

        assert prx['host'] is not None
        assert prx['port'] is not None and type(prx['port']) is int and prx['port'] > 0 and prx['port'] <= 65535

        log.debug("connecting to %s proxy: %s:%d" % (self.txtType, prx['host'], prx['port']))
        # socks proxy type can be socks.SOCKS5, socks.SOCKS4, socks.HTTP
        try:
            # if 
            if (prx['type'] is not 'http' and prx['username'] is not None and prx['password'] is not None):
                self.s.set_proxy(self.type, prx['host'], prx['port'], True, prx['username'], prx['password'])
            else:
                self.s.set_proxy(self.type, prx['host'], prx['port'], True)
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

    # main start function for threading.Thread
    def run(self):
        assert self.e is not None

        self.pool.acquire()
        res = None

        log.debug("adding thread %s to pool" % self.getName())

        if (self.s is None):
            self.createSocket(self.prx)

        res = self.makeRequest(self.domain, self.url, self.port, self.method, self.headers, self.postdata)

        log.debug("Closing thread: %s" % self.getName())
        self.pool.release()
        # thread

        return res

    def makeRequest(self, host, url="/", port=80, method='GET', headers=None, postdata=None):
        assert self.e is not None
        evSet = self.e.wait()  # noqa: F841
        # log.debug("Generating raw http request")
        self.s.connect((host, port))

        if headers is None:
            headers = {
                    "Accept": "*/*",
                    "User-Agent": self.useragent
            }

        req = self.rawHttpReq(host, url, method, headers, postdata)

        self.s.sendall(req.encode())

        h = []
        body = []
        p = HttpParser()
        tlen = 0

        while True:
            data = self.s.recv(2048)

            if not data:
                break

            rlen = len(data)
            tlen += rlen
            nparsed = p.execute(data, rlen)
            assert nparsed == rlen

            if p.is_headers_complete():
                h = p.get_headers()
                # log.debug(p.get_headers())
            if p.is_partial_body():
                body.append(p.recv_body())

            if p.is_message_complete():
                break

        self.s.close()
        self.q.put({'status': p.get_status_code(), 'length': tlen, 'headers': h, 'body': body, 'request': req})

    # creates raw http request header
    def rawHttpReq(
            self,
            host,
            url="/",
            method="GET",
            headers=None,
            postdata=None
    ):

        assert host is not None

        log.debug("Building request for: %s%s" % (host, url))

        req = "%s %s HTTP/1.1\r\n" % (method, url)
        req += "Host: %s\r\n" % (host)

        for k, v in headers.iteritems():
            req += "%s: %s\r\n" % (k, v)

        if postdata is not None:
            req += "Content-Length: %s\r\n" % str(len(postdata))

        if (self.txtType == 'http' and self.prx['username'] is not None and self.prx['password'] is not None):
            req += "Proxy-Authorization: basic %s\r\n" % (str(base64.b64encode("%s:%s" % (self.prx['username'], self.prx['password']))))

        req += "\r\n"

        if postdata is not None:
            req += postdata
            req += "\r\n"

        log.debug("\n-- HTTP REQUEST ------>>\n%s\n<<--------- /HTTP REQUEST--\n" % (req))
        return req
