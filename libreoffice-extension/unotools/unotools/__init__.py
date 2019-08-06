# -*- coding: utf-8 -*-
import argparse
import logging
from os.path import isdir, isfile

try:
    from functools import singledispatch
except ImportError:  # under 3.3
    from singledispatch import singledispatch

from unotools.context import LocalContext, ScriptContext
from unotools.errors import ArgumentError, ConnectionError


class Pipe:
    def __init__(self, name: str):
        self.name = name


class Socket:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port


@singledispatch
def connect(identifier: str, **kwargs) -> ScriptContext:
    context = None
    try:
        local_context = LocalContext()
        option = kwargs.get('option')
        if option is not None:
            identifier = '{},{}'.format(identifier, option)
        conn_str = 'uno:{};urp;StarOffice.ComponentContext'.format(identifier)
        context = local_context.resolver.resolve(conn_str)
        if context:
            return ScriptContext(context)
    except Exception as e:
        msg = 'failed to connect: {}'.format((identifier, kwargs))
        raise ConnectionError(msg) from e

    raise ConnectionError('cannot connect: {}'.format((identifier, kwargs)))


@connect.register(Pipe)
def connect_with_pipe(pipe: Pipe, **kwargs) -> ScriptContext:
    return connect('pipe,name={}'.format(pipe.name), **kwargs)


@connect.register(Socket)
def connect_with_socket(socket: Socket, **kwargs) -> ScriptContext:
    identifier = 'socket,host={},port={}'.format(socket.host, socket.port)
    return connect(identifier, **kwargs)


def parse_argument(argv: list):
    """
    >>> argv = '-s server -p 8080 -a tcpNoDelay=1'.split()
    >>> parse_argument(argv)  # doctest: +NORMALIZE_WHITESPACE
    Namespace(datadirs=[], encoding='utf-8', file_=None, host='server',
              option='tcpNoDelay=1', outputdir='.', pipe=None, port=8080,
              verbose=False)
    """
    def validate_file_or_directory_existence(args):
        def validate(paths, validate_func):
            for path in paths:
                if path is not None and not validate_func(path):
                    raise ArgumentError('"{}" is not found'.format(path))
        validate([args.file_], isfile)
        validate(args.datadirs + [args.outputdir], isdir)

    parser = argparse.ArgumentParser()
    parser.set_defaults(datadirs=[], encoding='utf-8', file_=None,
                        host='localhost', option=None, outputdir='.',
                        pipe=None, port=8100, verbose=False)
    parser.add_argument('-a', '--option', dest='option',
                        metavar='OPTION', help='set option')
    parser.add_argument('-d', '--datadirs', dest='datadirs', nargs='*',
                        metavar='DATADIRS', help='set data directories')
    parser.add_argument('-e', '--encoding', dest='encoding',
                        metavar='ENCODING',
                        help='set encoding. default is utf-8')
    parser.add_argument('-f', '--file', dest='file_',
                        metavar='FILE', help='set OpenDocument file to read')
    parser.add_argument('-i', '--pipe', dest='pipe',
                        metavar='PIPE', help='set pipe name')
    parser.add_argument('-o', '--outputdir', dest='outputdir',
                        metavar='OUTPUTDIR', help='set output directory')
    parser.add_argument('-p', '--port', dest='port', type=int,
                        metavar='PORT_NUMBER', help='set port number')
    parser.add_argument('-s', '--host', dest='host', required=True,
                        metavar='HOST', help='set host name')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='set verbose mode')
    args = parser.parse_args(argv)
    validate_file_or_directory_existence(args)

    if args.verbose:
        logging.root.setLevel(logging.DEBUG)
    logging.debug('args: {0}'.format(args))
    return args
