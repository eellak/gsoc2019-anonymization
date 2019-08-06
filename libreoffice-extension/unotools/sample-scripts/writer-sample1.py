# -*- coding: utf-8 -*-
import sys
from os.path import join as pathjoin

from unotools import Socket, connect
from unotools.component.writer import Writer
from unotools.unohelper import convert_path_to_url


def writer_sample(args, context):
    writer = Writer(context)
    writer.set_string_to_end('world\n')
    writer.set_string_to_start('hello\n')

    base_path = convert_path_to_url(pathjoin(args.outputdir, 'sample'))
    writer.store_to_url(base_path + '.odt', 'FilterName', 'writer8')
    writer.store_to_url(base_path + '.doc', 'FilterName', 'MS Word 97')
    writer.store_to_url(base_path + '-writer.pdf',
                        'FilterName', 'writer_pdf_Export')
    writer.store_to_url(base_path + '-writer.html',
                        'FilterName', 'HTML (StarWriter)')

    writer.close(True)


if __name__ == '__main__':
    from unotools import parse_argument
    args = parse_argument(sys.argv[1:])
    context = connect(Socket(args.host, args.port), option=args.option)
    writer_sample(args, context)
