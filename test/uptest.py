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
s.createSocket("75.97.107.190", 37614)
print(s.connectHost("ip.nrx.co", 81))

s.makeRequest("ip.nrx.co", "/")

print("Done")
