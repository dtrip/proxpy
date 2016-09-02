#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import logging
import sys
import os

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR)

from proxpy import upstream, log  # noqa: E402, F401
l = logging.getLogger()
l.setLevel(logging.DEBUG)


proxy = {
        'type': 'socks5',
        'host': '127.0.0.1',
        'port': 9050,
        'username': None,
        'password': None
}

s = upstream.upstream(proxy, 'ip.nrx.co', '/', 81)

# s.createSocket("127.0.0.1", 9050)
# print(s.connectHost("ip.nrx.co", 81))

# s.makeRequest("ip.nrx.co", "/")
s.start()
# s.exit()

print("Done")
