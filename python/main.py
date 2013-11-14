#!/usr/bin/env python
# coding=utf-8
import root
import bottle
import sys

def main(args):
	debug = '--debug' in args
	
	bottle.debug(debug)
	bottle.run(app=root.middleware_app, reloader=debug)

if __name__ == "__main__":
	main(sys.argv)

