import sys
import getopt


def find_entities(ifile, ofile, method='delete', custom_patterns='conf.json'):
    exit(0)


def main(argv):
    inputfile = ''
    outputfile = ''
    method = ''
    custom_patterns = ''
    try:
        opts, args = getopt.getopt(
            argv, "hi:o:m:", ["ifile=", "ofile=", "method="])
    except getopt.GetoptError:
        print('Use: python3 token_matcher.py -i <inputfile> -o <outputfile> -m <method used choose between q(quick) or s(slow)> -c <custom_entity>')
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
            print('Use: python3 token_matcher.py -i <inputfile> -o <outputfile> -m <method used choose between q(quick) or s(slow)>')
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
    find_entities(inputfile, outputfile, method, custom_patterns)


if __name__ == "__main__":
    main(sys.argv[1:])
