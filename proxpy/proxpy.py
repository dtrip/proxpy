#!/usr/bin/env python

from __future__ import division, print_function

import sys
import traceback
from colorama import init, Fore, Back, Style

import arg
import config

class proxpy(object):
    def __init__(self):
 
        ap = arg.arg()
        self.args = ap.args
       
    def run(self):
    
        if (self.args['debug']):
            print("Debugging Enabled")



if __name__ == "__main__":
    try:
        p = proxpy()
        p.run()
    except Exception as e:
        print("\n%s%s%s[!] Error: %s\n\n%s%s%s\n" % (Style.BRIGHT, Back.RED, Fore.WHITE, str(e), Style.NORMAL, traceback.format_exc(), Style.RESET_ALL))




