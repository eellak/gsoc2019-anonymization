import sys
import getopt
import matcher_patterns


def matches_handler(matcher, doc, i, matches, method='delete'):
    pass


def file_to_text(ifile, format='.txt'):
    try:
        with open(ifile, 'r') as f:
            data = f.read().replace('\n', ' ')
            return data
    except FileNotFoundError as fnf_error:
        exit(fnf_error)


def find_entities(ifile, ofile, method='delete', configuration='conf.json'):
    import spacy
    from spacy.matcher import Matcher
    nlp = spacy.load('el_core_news_sm')
    matcher = Matcher(nlp.vocab)
    data = file_to_text(ifile, '.txt')
    doc = nlp(data)

    # You can pass as argument the match handler. This one will
    # delete be default the recognised entities in the text

    matcher_patterns.phone_number(matcher)
    matches = matcher(doc)
    print(matches)
    for i, my_match in enumerate(matches):
        [match_id, start, end] = my_match
        string_id = doc.vocab.strings[match_id]
        print(f'The {i+1} match as {string_id}:{doc[start:end]}')
    print(doc)
    exit(0)


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
    find_entities(inputfile, outputfile, method, custom_patterns)


if __name__ == "__main__":
    main(sys.argv[1:])
