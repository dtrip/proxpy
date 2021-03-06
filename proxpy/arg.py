#!/usr/bin/env python

# import logging
import argparse
import configparser
from proxpy import log

logger = log.log()
# log = logging.getLogger()


class arg(object):
    def __init__(self, p):
        self.proxpy = p
        self.parser = argparse
        self.args = None
        self.boolArgs = ['debug', 'daemon', 'dns', 'verbose', 'quiet']
 
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
                "debug": "False",
                "backlog": 50,
                "receive": 4096,
                "upstreams": "upstreams.conf",
                "log": "proxpy.log"
                }

        if args.config:
            config = configparser.SafeConfigParser()
            config.read([args.config])
            defaults = dict(config.items("General"))


        self.parser = argparse.ArgumentParser(parents=[confParser], description='Proxpy', formatter_class=argparse.RawDescriptionHelpFormatter)

        self.parser.set_defaults(**defaults)

        self.parser.add_argument('-a', '--auth', help='require auth for local proxy daemon', default=False, action='store_true')
        self.parser.add_argument('-b', '--backlog', help='number of pending connections queue will hold', metavar='N', type=int)
        self.parser.add_argument('-d', '--debug', help='output debugging information', action='store_true')
        self.parser.add_argument('-i', '--interface', help='Interface for proxy service to listen in on', type=str)
        self.parser.add_argument('-l', '--log', help='log file', metavar='FILE')
        self.parser.add_argument('-m', '--receive', help='maxium number of bytes proxy service will receive. Default: 4096', metavar='N', default=4096, type=int)

        self.parser.add_argument('-p', '--port', help='proxy service port', metavar='N', type=int)
        self.parser.add_argument('-q', '--quiet', help='suppress output', action='store_true')
        self.parser.add_argument('-r', '--dns', help='Perform DNS lookup\'s over SOCKS prxxy', action='store_true')
        self.parser.add_argument('-s', '--daemon', help='Enable Proxy deamon service', action='store_true')
        # self.parser.add_argument('-T', '--transparent', help='run proxy daemon as transparent proxy', action='store_true')
        self.parser.add_argument('-t', '--timeout', help="socket timeout in seconds", type=int)
        self.parser.add_argument('-u', '--upstreams', help='Config file containing list of upstream proxies', metavar='FILE')

        self.parser.add_argument('-v', '--verbose', help='Verbose output for debugging', action='store_true')

        self.args = vars(self.parser.parse_args())

        if (len(self.boolArgs) > 0):
            for k in self.boolArgs:
                self.args[k] = arg.setBoolean(self.args[k])
        

        # if verbose is set, also flips debug flag
        if self.args['verbose']:
            self.args['debug'] = True

        return True

    def argList(self):
        if self.args['debug']:
            for k,v in self.args.items():
                logger.debug("%s:\t%s (%s)" % (k,v, str(type(v))[7:-2]))

    @staticmethod
    def setBoolean(s):
        if (s is None):
            return False

        if (type(s) is bool):
            return s

        if (s.lower() == 'true'):
            return True
        else:
            return False
