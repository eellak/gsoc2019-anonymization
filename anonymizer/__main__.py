import sys
import getopt
from anonymizer import anonymize


def main(argv):
    inputfile = ''
    outputfile = ''
    method = ''
    custom_patterns = ''
    helptext = '''Use: python3 anonymizer.py
    -i <inputfile>
    -o <outputfile>
    -m <method used: choose between deletion and encryption>
    -c <config.json>'''

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:m:", ["ifile=", "ofile=", "method="])
    except getopt.GetoptError:
        print(helptext)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ["-i", "--ifile"]:
            inputfile = arg
        elif opt in ["-o", "--ofile"]:
            outputfile = arg
        elif opt in ["-m", "--method"]:
            method = arg
        elif opt in ["-c", "--config"]:
            configurations = arg
            custom_patterns = configurations
        else:
            print(helptext)
            sys.exit()

    # Create output file name
        if inputfile != '' and outputfile == '':
            extensions = ['.txt', '.odt']
            for extension in extensions:
                if extension in inputfile:
                    splitted = inputfile.split(extension)
                    outputfile = splitted[0] + '_anonymized' + extension

    # Load -d conf.json for custom patterns
    # Pass custom patterns to find_entities()
    anonymize.find_entities(inputfile, outputfile, method, custom_patterns)


if __name__ == "__main__":
    main(sys.argv[1:])
