#!/usr/bin/env python
import logging
import traceback
from colorama import Fore, Back, Style

import os
import sys
import proxpy
from proxpy import proxies
from proxpy import arg
# from proxpy import log
from proxpy import server
# sys.setdefaultencoding('utf-8')
logg = logging.getLogger()



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


class proxpyService(object):
    def __init__(self):
        ap = arg.arg(self)
        self.args = ap.args

        if self.args['debug']:
            logg.setLevel(logging.DEBUG)


        ap.argList()
        # p = parser.parser(self)
        self.proxies = proxies.proxies(self.args['upstreams'])

        if self.args['debug']:
            logg.debug("Debug enabled")

    def run(self):

        logg.info("Starting proxy service")

    
        self.server = server.server()
        self.server.run()


if __name__ == "__main__":
    try:
        p = proxpyService()
        p.run()
    except Exception as e:
        logg.critical("\n%s%s%s[!] Error: %s\n\n%s%s%s\n" % (Style.BRIGHT, Back.RED, Fore.WHITE, str(e), Style.NORMAL, traceback.format_exc(), Style.RESET_ALL))
    finally:
        print("\n")
