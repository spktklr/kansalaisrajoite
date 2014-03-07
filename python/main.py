#!/usr/bin/env python
# coding=utf-8
import argparse

import root
import bottle


application = root.middleware_app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug', help='enable debug mode and autoreload',
        action='store_true')
    parser.add_argument(
        '--host', help='set to 0.0.0.0 to listen on all interfaces',
        type=str, default='127.0.0.1')
    parser.add_argument(
        '--port', help='listen port',
        type=int, default=8080)
    args = parser.parse_args()

    bottle.debug(args.debug)
    bottle.run(app=application, reloader=args.debug,
               host=args.host, port=args.port)

if __name__ == "__main__":
    main()
