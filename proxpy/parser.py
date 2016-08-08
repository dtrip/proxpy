#!/usr/bin/env python

from __future__ import division, print_function

class parser(object):
    def __init__(self, p):
        self.proxpy = p
        self.rdata = []
        self.proxies = []
        self.__readFile()

    def __readFile(self):

        if (self.proxpy.args['debug']):
            print("Opening upstreams file for parsing: %s" % (self.proxpy.args['upstreams']))

        with open(self.proxpy.args['upstreams'], 'r') as f:
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
            pxs = parser.splitProxyString(px, self.proxpy.args['debug'])

            self.proxies.append({"type": pxs[0], "host": pxs[1], "port": pxs[2], "username": pxs[3], "password": pxs[4] })

    
    @staticmethod
    def splitProxyString(proxyString, debug=False): 
        
        splitTmp = proxyString.split("://")
        type = splitTmp[0].lower()

        if (type == 'https'):
            type = 'http'

        uname = ''
        passw = ''

        # if '@' is in connection string 
        # will parse username/password for proxy authentcation
        if ('@' in splitTmp[1]):
            authSplit = splitTmp[1].split("@")
            uname = authSplit[0].split(":")[0]
            passw = authSplit[0].split(":")[1]
            host = authSplit[1].split(":")[0]
            port = authSplit[1].split(":")[1]

            if (debug):
                umask = "*" * len(uname)
                pmask = "*" * len(passw)
                print("Proxy Parsed. Type: %s Host: %s Port: %s Username: %s Password: %s" % (type, host, port, umask, pmask))

        else:
            host = splitTmp[1].split(":")[0]
            port = splitTmp[1].split(":")[1]

            if (debug):
                print("Proxy Parsed. Type: %s Host: %s Port: %s" % (type, host, port))

        return [type, host, port, uname, passw]

