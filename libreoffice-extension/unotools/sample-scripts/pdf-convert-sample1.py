# -*- coding: utf-8 -*-
import sys
from os.path import basename, join as pathjoin, splitext

from unotools import Socket, connect
from unotools.component.calc import Calc
from unotools.component.writer import Writer
from unotools.unohelper import convert_path_to_url


def get_component(args, context):
    _, ext = splitext(args.file_)
    url = convert_path_to_url(args.file_)
    if ext == '.odt':
        component = Writer(context, url)
    elif ext == '.ods':
        component = Calc(context, url)
    else:
        raise ValueError('Supported file type are [odt|ods]: {}'.format(ext))
    return component


def convert_pdf(args, context):
    component = get_component(args, context)
    filename = basename(args.file_).split('.')[0] + '.pdf'
    url = convert_path_to_url(pathjoin(args.outputdir, filename))
    property_ = '{}_pdf_Export'.format(component.__class__.__name__.lower())
    component.store_to_url(url, 'FilterName', property_)
    component.close(True)


if __name__ == '__main__':
    from unotools import parse_argument
    args = parse_argument(sys.argv[1:])
    if args.file_ is None:
        usage = 'Usage: python {} -s localhost -f path/to/file.[odt|ods]'
        print(usage.format(__file__))

    context = connect(Socket(args.host, args.port), option=args.option)
    convert_pdf(args, context)
