import sys
import getopt
import spacy
from spacy.matcher import Matcher
from termcolor import colored
from anonymizer import matcher_patterns
from anonymizer.external_functions import official_json
from anonymizer.external_functions import fix_pattern
from anonymizer.external_functions import sort_by_start


def read_patterns(ifile=''):
    with open(ifile, 'r') as f:
        import json
        data = f.read().replace('\n', ' ')

        # Function that returns json object but
        # replaces \ with <#ec>

        json_file = official_json(data)

        return json_file
    raise NameError('patterns.json file can not be found.')


def entity_type_convertion(data, doc):
    results = []
    for match_id, start, end in data:
        entity_name = doc.vocab.strings[match_id]
        found_by_spacy = True
        span = doc[start:end]
        results.append([entity_name, span, span,
                        start, end, found_by_spacy])
    return(results)


def matches_handler(matcher, doc, i, matches, method='delete'):
    pass


def file_to_text(ifile, format='.txt'):
    try:
        with open(ifile, 'r') as f:
            data = f.read().replace('\n', ' ')
            return data
    except FileNotFoundError as fnf_error:
        exit(fnf_error)


def find_entities(ifile, ofile, method='delete', patterns_file='patterns.json', in_order=True):

    nlp = spacy.load('el_core_news_sm')
    matcher = Matcher(nlp.vocab)
    data = file_to_text(ifile, '.txt')
    doc = nlp(data)
    data = str(doc)

    # READ CONFIGURATION FILE
    #
    conf_json = read_patterns(patterns_file)
    '''
        --- ENTITY LIST EXPLANATION ---
        entities = [entity_name, entity_value,
            span/word, start, end, found_by_spacy]

        We will use found_by_spacy bool to access data either via
        doc[start:end] if True else str(doc)[start:end] .

        Span/word is the word just the way it was found into the text
        while entity_value is the value extracted through specific
        algorithms each time.

        Some times these to might have the same value.
    '''
    entities = []
    try:
        [x, y] = conf_json['matcher'].items()
    except:
        raise NameError('Corrupted patterns file.')

    for matcher, value in conf_json['matcher'].items():
        if value['active'] == 'False':
            continue
        custom_pattern_method = getattr(matcher_patterns, matcher)
        # Call function with the proper parameters
        results = custom_pattern_method(
            data=data, pattern=fix_pattern(value['pattern']))
        if results != None:
            entities += results

    if in_order == True:
        entities.sort(key=sort_by_start)

    # Display
    for element in entities:
        print('[', colored(element[0], 'yellow'), ',', colored(
            element[1], 'blue'), ',', colored(element[2], 'cyan'),
            ',', element[3],
            ']',)
