from __future__ import division
import argparse

import bottle
from bottle import static_file, route

app = application = bottle.default_app()


@route('/')
def _index_html():
    return static_file('index.html', root='./static')


@route('/file/<filename:path>')
def static(filename):
    return static_file(filename, root='./static')


def parse_args():
    parser = argparse.ArgumentParser(description='HTTP server for Mini-Debating AI')
    parser.add_argument("--port", type=int, default=8111, help="server port")
    return parser.parse_args()


if __name__ == "__main__":
    opt = parse_args()
    bottle.run(host='0.0.0.0', port=opt.port)
