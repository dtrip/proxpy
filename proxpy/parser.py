#!/usr/bin/env python
from __future__ import division, print_function
import logging

log = logging.getLogger()


class parser(object):
    def __init__(self, conf):
        self.rdata = []
        self.proxies = []
        self.conf = conf
        self.__readFile()

    def __readFile(self):

        log.debug("Opening upstreams file for parsing: %s" % (self.conf))

        with open(self.conf, 'r') as f:
            for line in f:
                line = line.strip('\t\n\r')
                if (line[0:1] is not '#' and len(line) > 0):
                    # if (self.proxpy.args['debug']): 
                        # print("Adding proxy to list: %s" % line)
                    self.rdata.append(line)

        self.__parseRawProxyArray()

    def __parseRawProxyArray(self):
        if (len(self.rdata) == 0):
            raise ValueError("No data proxy list data to parse")

        for px in self.rdata:
            pxs = parser.splitProxyString(px)

            self.proxies.append({"type": pxs[0], "host": pxs[1], "port": pxs[2], "username": pxs[3], "password": pxs[4]})

            if (pxs[3] is None):
                pxs[3] = ''

            if (pxs[4] is None):
                pxs[4] = ''

            log.debug("Proxy Parsed. Type: %s Host: %s Port: %s Username: %s Password: %s" % (pxs[0], pxs[1], pxs[2], "*" * len(pxs[3]), "*" * len(pxs[4])))

    @staticmethod
    def splitProxyString(proxyString): 
        splitTmp = proxyString.split("://")
        type = splitTmp[0].lower()

        if (type == 'https'):
            type = 'http'

        uname = None
        passw = None

        # if '@' is in connection string 
        # will parse username/password for proxy authentcation
        if ('@' in splitTmp[1]):
            authSplit = splitTmp[1].split("@")
            uname = authSplit[0].split(":")[0]
            passw = authSplit[0].split(":")[1]
            host = authSplit[1].split(":")[0]
            port = authSplit[1].split(":")[1]
        else:
            host = splitTmp[1].split(":")[0]
            port = splitTmp[1].split(":")[1]

        return [type, host, int(port), uname, passw]
