#!/usr/bin/env python
from __future__ import division, print_function
from colorama import Fore, Style
import logging
import traceback


class log(logging.getLoggerClass()):
    __FORMAT = {
        'fmt': ('[%(levelname).1s] %(message)s'),
        'datefmt': '%Y-%m-%d %H-%M-%S' 
    }

    def __init__(self, format=__FORMAT):
        formatter = LogFormatter()
        self.root.setLevel(logging.DEBUG)
        self.root.handlers = []
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(formatter)
        self.root.addHandler(self.handler)

    def info(self, msg, *vars):
        self.root.info(msg % vars)

    def debug(self, msg, *vars):
        self.root.debug(msg % vars)

    def warning(self, msg, *vars):
        self.root.warning(msg % vars)

    def error(self, msg, *vars):
        self.root.error(msg % vars)


class LogFormatter(logging.Formatter):
    err_fmt = Style.BRIGHT + Fore.RED + "[E]" + Style.RESET_ALL + " %(module)s:%(lineno)s %(msg)s" + str(traceback.print_exc())
    dbg_fmt = Style.BRIGHT + Fore.BLUE + "[*]" + Style.RESET_ALL + " %(msg)s"
    inf_fmt = Style.BRIGHT + Fore.GREEN + "[!]" + Style.RESET_ALL + " %(msg)s"
    wrn_fmt = Style.BRIGHT + Fore.YELLOW + "[W]" + Style.RESET_ALL + " %(msg)s"

    def __init__(self, fmt="%(levelno): %(msg)s"):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):

        format_orig = self._fmt

        if record.levelno == logging.DEBUG:
            self._fmt = LogFormatter.dbg_fmt
        elif record.levelno == logging.INFO:
            self._fmt = LogFormatter.inf_fmt
        elif record.levelno == logging.ERROR:
            self._fmt = LogFormatter.err_fmt
        elif record.levelno == logging.WARNING:
            self._fmt = LogFormatter.wrn_fmt

        result = logging.Formatter.format(self, record)
        self._fmt = format_orig

        return result 
