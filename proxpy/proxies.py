#!/usr/bin/env python
from __future__ import division, print_function
import parser
import logging
import random

log = logging.getLogger()


class proxies(object):
    def __init__(self, conf):
        assert type(conf) is not None

        self.conf = conf

        p = parser.parser(conf)
        self.proxies = p.proxies

    def getRandom(self):
        return random.choice(self.proxies)

    def getProxy(self, k):
        log.debug("Getting a proxy server")
        return self.proxies[k]
