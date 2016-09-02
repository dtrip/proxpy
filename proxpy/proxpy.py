#!/usr/bin/env python
from __future__ import division, print_function

# import sys
import traceback
from colorama import Fore, Back, Style

# import os
import arg
# import config
import parser
import server
import logging
import proxies
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger()



print(Fore.YELLOW + Style.BRIGHT + '''
 ____                                         
/\  _`\                                        
\ \ \L\ \_ __   ___   __  _  _____   __  __    
 \ \ ,__/\`'__\/ __`\/\ \/'\/\ '__`\/\ \/\ \   
  \ \ \/\ \ \//\ \L\ \/>  </\ \ \L\ \ \ \_\ \  
   \ \_\ \ \_\\\\ \____//\_/\_\\\\ \ ,__/\/`____ \ 
    \/_/  \/_/ \/___/ \//\/_/ \ \ \/  `/___/> \\
                               \ \_\     /\___/
                                \/_/     \/__/ 

''' + Style.RESET_ALL)


class proxpy(object):
    def __init__(self):
        ap = arg.arg(self)
        self.args = ap.args

        ap.argList()

        # p = parser.parser(self)
        self.proxies = proxies.proxies(self.args['upstreams'])

        logger.setLevel(logging.DEBUG)

    def run(self):

        logging.info("Starting proxy service")

    
        self.server = server.server()
        self.server.run()
        # self.server = server()
        # self.server.listenClients()


if __name__ == "__main__":
    try:
        p = proxpy()
        p.run()
    except Exception as e:
        logging.exception("\n%s%s%s[!] Error: %s\n\n%s%s%s\n" % (Style.BRIGHT, Back.RED, Fore.WHITE, str(e), Style.NORMAL, traceback.format_exc(), Style.RESET_ALL))
