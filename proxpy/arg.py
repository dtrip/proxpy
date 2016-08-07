#!/usr/bin/env python

from __future__ import division, print_function

import argparse

class arg(object):
    def __init__(self):
        self.parser = argparse
        self.args = None
 
        pass

    def __parseArgs(self):

        self.parser = argparse.ArgumentParser(description='Proxpy')

        self.parser.add_argument('-c', '--config', help='Specify config file to use', type=str)
        self.parser.add_argument('-v', '--verbose', help='Verbose output for debugging', action='store_true')

        self.args = vars(self.parser.parse_args())


        return True
