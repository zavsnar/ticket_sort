#!/usr/bin/env python

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

def format_response(params_dict):
    for k, v in params_dict.items():
        yield '{0} is {1}\n'.format(k,v[0])

def echo(environ, start_response):
    params_dict = parse_qs(environ['QUERY_STRING'])
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return format_response(params_dict)

def not_found(environ, start_response):
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']

def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    if 'test' == path:
        return echo(environ, start_response)

    return not_found(environ, start_response)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 9090, application)
    srv.serve_forever()