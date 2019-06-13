import sys
import getopt
from anonymizer import anonymize
from anonymizer.external_functions import create_output_file_name
import argparse
import os.path


def main(argv):
    inputfile = ''
    outputfile = ''
    method = ''
    configuration_file = 'anonymizer/conf.json'
    helptext = '''Use: python3 anonymizer.py
    -i <inputfile>
    -o <outputfile>
    -m <method used: choose between deletion and encryption>
    -c <config.json>'''

    parser = argparse.ArgumentParser(
        description='Anonymize file', usage=helptext)
    parser.add_argument('-i', '--ifile', help='Input file',
                        type=str, required=True)
    parser.add_argument('-o', '--ofile', help='Output file',
                        type=str, required=False)

    parser.add_argument('-c', '--conf_file',
                        help='Configuration file', type=str, required=False)

    parser.add_argument('-m', '--method',
                        help='Which method is applied to the identified data')
    args = parser.parse_args()

    if args.ifile != None:
        inputfile = args.ifile

    if args.ofile != None:
        outputfile = args.ofile
    else:
        outputfile = create_output_file_name(inputfile)

    if args.method != None:
        method = args.method

    if args.conf_file != None:
        configuration_file = args.conf_file
    else:
        # If the service can not track conf.json
        if not os.path.exists(configuration_file):
            raise NameError(
                "Please make sure that the conf.json file's path is: anonymizer/conf.json")

    # Load -d conf.json for custom patterns
    # Pass custom patterns to find_entities()
    anonymize.find_entities(inputfile, outputfile, method,
                            configuration_file=configuration_file)


if __name__ == "__main__":
    main(sys.argv[1:])
