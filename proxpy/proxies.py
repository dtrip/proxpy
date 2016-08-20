#!/usr/bin/env python
from __future__ import division, print_function
import parser
import logging

log = logging.getLogger()


class proxies(object):
    def __init__(self, conf):
        assert type(conf) is not None

        self.conf = conf

        p = parser.parser(conf)
        self.proxies = p.proxies

    def getProxy(self):
        log.debug("Getting a proxy server")
        pass
