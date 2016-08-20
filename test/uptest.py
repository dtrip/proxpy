#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import sys
import os
import logging

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR)

from proxpy import upstream
# help(proxpy)
# print(proxpy)
s = upstream.upstream()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

# file handler
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# console logging
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
# logger.addHandler(ch)
logger.addHandler(ch)



logger.debug("Connecting to socket")
s.createSocket("127.0.0.1", 9050)
print(s.connectHost("ip.nrx.co", 81))

s.makeRequest("ip.nrx.co", "/")

print("Done")
