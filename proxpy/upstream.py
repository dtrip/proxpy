#!/usr/bin/env python

from __future__ import division, print_function
import urllib2
import socks
import types
import numbers
from sockshandler import SocksiPyHandler

class upstream(object):

    def __init__(self, p):
        self.proxpy = p
        # self.opener = None
        # self.socksHandler = None
        self.s = None
 

    def createSocket(self, host, port):
        self.s = socks.socksocket()

        assert host is not None
        assert port is not None and type(port) is int and port > 0 and port <= 65535

        self.proxpy.log.debug("connecting to socks proxy: %s:%d", (host, port))
        # socks proxy type can be socks.SOCKS5, socks.SOCKS4, socks.HTTP
        try:
            self.s.set_proxy(socks.SOCKS5, host, port, True)
        except self.s.ProxyConnectionError as e:
            print(str(e))
            raise
        except self.s.GeneralProxyError as e:
            print(str(e))
            raise
        except Exception as e:
            print(str(e))
            raise

        return True

    def closeSocket(self):
        return self.s.close()

    
    def connectHost(self, url, port=80): 
        
        assert url is not None

        self.proxpy.log.debug("Making request to %s:%d", (url, port))

        # return self.opener.open(url)
        try:
            return self.s.connect((url,port))
        except self.s.ProxyConnectionError as e:
            raise
        except self.s.GeneralProxyError as e:
            raise
        except Exception as e:
            raise
        return False

    def makeRequest(self, host, url="/"):
        req = self.rawHttpReq(host)
        self.s.sendall(req)
        status = self.s.recv(2048)

        self.proxpy.log.debug("Status: %s", (status))
        return True


    def rawHttpReq(self, host, url="/", userAgent="Proxpy", acpt="*/*"):

        assert host is not None

        req = "GET %s HTTP/1.1\r\n" % (url)
        req += "Host: %s\r\n" % (host)
        req += "User-Agent: %s\r\n" % (userAgent)
        req += "Accept: %s\r\n" % (acpt)
        req += "\r\n"

        self.proxpy.log.debug(req)
        return req.encode()
