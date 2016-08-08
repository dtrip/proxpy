#!/usr/bin/env python

from __future__ import division, print_function

import argparse
import ConfigParser

class arg(object):
    def __init__(self):
        self.parser = argparse
        self.args = None
 
        self.__parseArgs()

    def __parseArgs(self):

        confParser = argparse.ArgumentParser(
                add_help=False
                )

        confParser.add_argument('-c', '--config', help='Specify config file to use. Default: proxpy.conf', metavar="FILE", default="proxpy.conf")

        args, remaining_argv = confParser.parse_known_args()



        defaults = {
                "interface": "127.0.0.1",
                "port": "8080",
                "debug": "False"
                }

        if args.config:
            config = ConfigParser.SafeConfigParser()
            config.read([args.config])
            defaults = dict(config.items("General"))


        self.parser = argparse.ArgumentParser(parents=[confParser], description='Proxpy', formatter_class=argparse.RawDescriptionHelpFormatter)

        self.parser.set_defaults(**defaults)

        self.parser.add_argument('-a', '--local-auth', help='require auth for local proxy daemon', default=False, action='store_true')
        self.parser.add_argument('-d', '--debug', help='output debugging information', action='store_true')
        self.parser.add_argument('-i', '--interface', help='Interface for proxy service to listen in on', type=str)

        self.parser.add_argument('-p', '--port', help='proxy service port', metavar='N', type=int)
        self.parser.add_argument('-r', '--remote-dns', help='Perform DNS lookup\'s over SOCKS proxxy', action='store_true')
        self.parser.add_argument('-s', '--daemon', help='Enable Proxy deamon service', action='store_true')
        self.parser.add_argument('-t', '--transparent', help='run proxy daemon as transparent proxy', action='store_true')

        self.parser.add_argument('-v', '--verbose', help='Verbose output for debugging', action='store_true')

        self.args = vars(self.parser.parse_args())


        return True
