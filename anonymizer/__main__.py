import sys
import getopt
from anonymizer import anonymize
from anonymizer.external_functions import create_output_file_name
import argparse
import os.path
import json


def main(argv):
    inputfile = ''
    outputfile = ''
    method = ''
    conf_file = 'anonymizer/conf.json'
    # in_order = True
    patterns_file = 'anonymizer/patterns.json'
    helptext = '''Use: python3 anonymizer.py
    -i <inputfile>
    -o <outputfile>
    -m <method used: choose between deletion and encryption>
    -p <patterns.json>
    -l <True,False: choose in line with text results>
    -c <conf.json>'''

    parser = argparse.ArgumentParser(
        description='Anonymize file', usage=helptext)
    parser.add_argument('-i', '--ifile', help='Input file',
                        type=str, required=True)

    parser.add_argument('-o', '--ofile', help='Output file',
                        type=str, required=False)

    parser.add_argument('-c', '--conf_file',
                        help='Configuration file', type=str, required=False)

    parser.add_argument('-p', '--patterns_file',
                        help='Patterns file', type=str, required=False)

    parser.add_argument('-m', '--method',
                        help='Which method is applied to the identified data')

    parser.add_argument('-l', '--in_order',
                        help='Show results in line/order with the text')
    args = parser.parse_args()

    # If given configuration file check that it exists
    #
    if args.conf_file != None:
        conf_file = args.conf_file
        if not os.path.exists(conf_file):
            raise NameError(
                f'Please make sure that the file ({conf_file}) exists.')
    else:
        # If the service can not track conf.json
        if not os.path.exists(conf_file):
            raise NameError(
                "Please make sure that the conf.json file's path is: anonymizer/conf.json")

    with open(conf_file, mode='r') as cf:
        data = cf.read().replace('\n', '')
        conf_json = json.loads(data)

    if args.ifile != None:
        inputfile = args.ifile

    if args.ofile != None:
        outputfile = args.ofile
    else:
        outputfile = create_output_file_name(inputfile)

    if args.method != None:
        method = args.method

    if args.in_order != None:
        if args.in_order in [True, False]:
            in_order = args.in_order
        else:
            raise NameError('--in_order: Choose between: True,False')
    else:
        in_order = True if conf_json['general']['in_order']['value'] == 'True' else False
    # If given patterns file check that it exists
    #
    if args.patterns_file != None:
        patterns_file = args.patterns_file
        if not os.path.exists(patterns_file):
            raise NameError(
                f'Please make sure that the file ({patterns_file}) exists.')
    else:
        # If the service can not track patterns.json
        patterns_file = conf_json['paths']['patterns.json']
        if not os.path.exists(patterns_file):
            raise NameError(
                f"Please make sure that the patterns.json file's path is: {patterns_file}")

    # Load -d patterns.json for custom patterns
    # Pass custom patterns to find_entities()
    anonymize.find_entities(inputfile, outputfile, method,
                            patterns_file=patterns_file, in_order=in_order)


if __name__ == "__main__":
    main(sys.argv[1:])
