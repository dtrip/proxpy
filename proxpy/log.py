#!/usr/bin/env python3
from colorama import Fore, Style, Back
import logging

class log(logging.getLoggerClass()):
    __FORMAT = {
        'fmt': ('[%(levelname).1s] %(message)s'),
        'datefmt': '%Y-%m-%d %H-%M-%S' 
    }

    def __init__(self, format=__FORMAT):

        # self.root._log.addLevelName(QUESTIONLVL, "QUESTION")
        formatter = LogFormatter()
        self.root.setLevel(logging.INFO)
        self.root.handlers = []
        # self.handler = logging.StreamHandler()
        self.handler = logging.FileHandler('proxpy.log')
        self.handler.setFormatter(formatter)
        self.root.addHandler(self.handler)

        # self.root.question = self.question

    def info(self, msg, *vars):
        self.root.info(msg % vars)

    def debug(self, msg, *vars):
        self.root.debug(msg % vars)

    def warning(self, msg, *vars):
        self.root.warning(msg % vars)

    def error(self, msg, *vars):
        self.root.error(msg % vars)

    # def question(self, msg, *args, **kws):
    #     if self.isEnabledFor(QUESTIONLVL):
    #         self.root._log(QUESTIONLVL, msg, args, **kws)
    #     else:
    #         self.root.info(msg % vars)


class LogFormatter(logging.Formatter):
    err_fmt = ("[{0}{1}E{2}] {3}{4}[%(module)s %(lineno)s] %(msg)s {5}".format(Style.BRIGHT, Fore.RED, Style.RESET_ALL, Style.BRIGHT, Fore.RED, Style.RESET_ALL))
    cri_fmt = ("[{0}{1}C{2}] {3}{4}{5}[%(module)s %(lineno)s] %(msg)s {6}".format(Style.BRIGHT, Fore.RED, Style.RESET_ALL, Style.BRIGHT, Fore.WHITE, Back.RED, Style.RESET_ALL))
    dbg_fmt = ("[{0}{1}*{2}] %(msg)s".format(Style.BRIGHT, Fore.CYAN, Style.RESET_ALL))
    # inf_fmt = "[" + Style.BRIGHT + Fore.BLUE + "I" + Style.RESET_ALL + "] %(msg)s"
    inf_fmt = ("[{0}{1}I{2}] %(msg)s".format(Style.BRIGHT, Fore.BLUE, Style.RESET_ALL))
    wrn_fmt = ("[{0}{1}W{2}] %(msg)s".format(Style.BRIGHT, Fore.YELLOW, Style.RESET_ALL))
    # qst_fmt = "[" + Style.BRIGHT + Fore.CYAN + "?" + Style.RESET_ALL + "] %(msg)s"

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
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
        elif record.levelno == logging.CRITICAL:
            self._fmt = LogFormatter.cri_fmt
        # elif record.levelno == QUESTIONLVL:
            # self._fmt = LogFormatter.qst_fmt
        # logging.Formatter.format(self, self._fmt)
        logging.Formatter.__init__(self, self._fmt)

        return super(LogFormatter, self).format(record)
        # result = logging.Formatter.format(self, record)
        # self._fmt = format_orig
        # return result 
