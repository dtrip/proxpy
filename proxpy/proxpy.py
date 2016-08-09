#!/usr/bin/env python
from __future__ import division, print_function

import sys
import traceback
from colorama import init, Fore, Back, Style

import os
import arg
import config
import parser
import server
import log

# if os.fork():
    # sys.exit()

class proxpy(object):
    def __init__(self):
 
        ap = arg.arg()
        self.args = ap.args

        p = parser.parser(self)
        self.proxies = p.proxies

        # l = log.log(self)
        self.log = log.log(self)
        self.log.info("test info")

       
    def run(self):
    
        if (self.args['debug']):
            print("Debugging Enabled")

        print("Starting proxy server")

        self.server = server.server(self)


if __name__ == "__main__":
    try:
        p = proxpy()
        p.run()
    except Exception as e:
        print("\n%s%s%s[!] Error: %s\n\n%s%s%s\n" % (Style.BRIGHT, Back.RED, Fore.WHITE, str(e), Style.NORMAL, traceback.format_exc(), Style.RESET_ALL))




