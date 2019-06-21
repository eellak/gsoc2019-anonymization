import sys
import getopt
from anonymizer.anonymize import find_entities
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
    '''

    parser = argparse.ArgumentParser(
        description='Anonymize file', usage=helptext)
    parser.add_argument('-i',
                        '--ifile',
                        help='Input file',
                        type=str,
                        required=False)

    parser.add_argument('-o',
                        '--ofile',
                        help='Output file',
                        type=str,
                        required=False)

    parser.add_argument('-p',
                        '--patterns_file',
                        help='Patterns file',
                        type=str,
                        required=False)

    parser.add_argument('-m',
                        '--method',
                        help='Which method is applied to the identified data', type=str,
                        required=False)

    parser.add_argument('-l',
                        '--in_order',
                        help='Show results in line/order with the text',
                        required=False)

    parser.add_argument('-f',
                        '--folder',
                        help='Anonymize all files in folder',
                        type=str,
                        required=False)
    args = parser.parse_args()

    # If given configuration file check that it exists
    #
    # If the service can not track conf.json
    if not os.path.exists(conf_file):
        raise NameError(
            "Please make sure that the conf.json file's path is: anonymizer/conf.json")

    with open(conf_file, mode='r') as cf:
        data = cf.read().replace('\n', '')
        conf_json = json.loads(data)

    inputfile = args.ifile

    if args.ofile != None:
        outputfile = args.ofile
    elif inputfile != None:
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
        patterns_file = conf_json['paths']['patterns']
        if not os.path.exists(patterns_file):
            raise NameError(
                f"Please make sure that the patterns file's path is: {patterns_file}")

    if (inputfile != None):
        # Pass custom patterns to find_entities()
        find_entities(ifile=inputfile,
                      ofile=outputfile,
                      method=method,
                      patterns_file=patterns_file,
                      in_order=in_order)

    if args.folder != None:
        folder = args.folder
        if not os.path.exists(folder):
            raise NameError(f"This folder ({folder}) doesn't exist.")
        files = []
        for file in os.listdir(folder):
            if file.endswith(".txt") or file.endswith(".odt"):
                files.append(folder + file)
        # print(files)
        for file in files:
            # print(file)
            find_entities(ifile=file,
                          ofile=create_output_file_name(file),
                          method=method,
                          patterns_file=patterns_file,
                          in_order=in_order)


if __name__ == "__main__":
    main(sys.argv[1:])
