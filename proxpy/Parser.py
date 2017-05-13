#!/usr/bin/env python3
import logging
import re

log = logging.getLogger()

class Parser(object):
    def __init__(self):
        pass

    @staticmethod
    def getHttpMethod(req):
        req = req.decode('utf-8')

        log.debug("Getting HTTP method for request:\n %s" % (req))

        firstline = req.splitlines()[0]

        flsplit = firstline.split(' ')

        mthd = flsplit[0]

        log.debug("Parsed Method: %s" % (mthd))

        return mthd


    @staticmethod
    def getReqPath(req):
        if isinstance(req, (bytes, bytearray)):
            req = req.decode('utf-8')

        firstline = req.splitlines()[0]

        reqPath = firstline.split(' ')[1]

        log.debug("Parsed Request Path: %s" % (reqPath))

        return reqPath


    @staticmethod
    def checkReqestAbsolute(uriPath):

        pattern = re.compile("^http(s)?://.*$")

        if pattern.match(uriPath):
            return True

        return False

    @staticmethod
    def addHttpsToReqPath(req):

        if isinstance(req, (bytes, bytearray)):
            req = req.decode('utf-8')

        rep = re.sub('CONNECT\s', 'CONNECT https://', req)

        log.debug("Added https://\n\n%s" % (rep))

        return str.encode(rep)
