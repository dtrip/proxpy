#!/usr/bin/env python
from __future__ import division, print_function
import logging

class log(object):

    def __init__(self, p):
        self.proxpy = p
        self.log = logging.basicConfig(filename=self.proxpy.args['log'], level=logging.INFO)

    def into(self, msg, vars=None):
        logging.info(msg % vars)

    def debug(self, msg, vars=None):
        logging.debug(msg % vars)

    def error(self, msg, vars=None):
        logging.error(msg % vars)

