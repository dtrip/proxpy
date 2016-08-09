#!/usr/bin/env python
from __future__ import division, print_function

from colorama import init, Fore, Back, Style
import logging

class log(object):

    def __init__(self, p):
        self.proxpy = p
 
        self.log = logging.basicConfig(filename=self.proxpy.args['log'], 
                level=(logging.DEBUG if self.proxpy.args['debug'] else logging.INFO))

    def info(self, msg, vars=()):
        logging.info(msg % (vars))
        msg = Fore.GREEN + Style.BRIGHT + "[!] " + Style.RESET_ALL + msg

        if (self.proxpy.args['quiet'] is not True):
            print(msg % (vars))

    def debug(self, msg, vars=()):
        logging.debug(msg % (vars))
        msg = Fore.BLUE + Style.BRIGHT + "[*] " + Style.RESET_ALL + msg

        if (self.proxpy.args['quiet'] is not True):
            print(msg % (vars))

    def warning(self, msg, vars=()):
        logging.warning(msg % (vars))

        msg = Fore.YELLOW + Style.BRIGHT + "[*] " + Style.RESET_ALL + msg

        if (self.proxpy.args['quiet'] is not True):
            print(msg % (vars))

    def error(self, msg, vars=()):
        logging.error(msg % (vars))

        msg = Fore.RED + Style.BRIGHT + "[*] " + Style.RESET_ALL + msg

        if (self.proxpy.args['quiet'] is not True):
            print(msg % (vars))



