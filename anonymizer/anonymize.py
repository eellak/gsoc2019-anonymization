import sys
import getopt
from os import system as runShell
from termcolor import colored
from anonymizer import matcher_patterns
from anonymizer.external_functions import official_json
from anonymizer.external_functions import fix_patterns, fix_pattern
from anonymizer.external_functions import sort_by_start
from anonymizer.external_functions import create_output_file_name


def anonymize_element(element, method=['strict', '*', 'True']):

    [method_type,
     symbol,
     length_replace] = method
    if len(symbol) > 1:
        symbol = symbol[0]
    span = element[2]
    s = element[3]
    e = element[4]
    if method_type.lower() in ['strict', 's']:
        if length_replace.lower() in ['true', 't']:
            l = len(span)
        else:
            try:
                l = int(float(length_replace))
                if l > len(span):
                    l = len(span)
            except:
                raise NameError(f'Not acceptable lenght: {length_replace}')
        rep = ''
        for i in range(l):
            rep += symbol
        # Fill the remaining gap with spaces
        # This keeps the alignment
        for i in range(len(span) - l):
            rep += ' '
        return rep


def read_patterns(ifile=''):
    import os
    cwd = os.path.abspath(__file__)
    ifile = os.path.dirname(cwd) + '/' + ifile
    with open(ifile, 'r') as f:
        import json
        data = f.read().replace('\n', ' ')

        # Function that returns json object but
        # replaces \ with <#ec>

        json_file = official_json(data)

        return json_file
    raise NameError('patterns file can not be found.')


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


def read_data_from_file(ifile, format='txt'):
    if format == 'txt':
        try:
            with open(ifile, 'r') as f:
                data = f.read()
                replaced = []
                for i, letter in enumerate(data):
                    if letter in ['\n', '\t', '\r']:
                        replaced.append([i, letter])
                data = data.replace('\n', ' ').replace(
                    '\t', ' ').replace('\r', ' ')
                return [data, replaced]
        except FileNotFoundError as fnf_error:
            exit(fnf_error)
    else:

        tempfile = ifile[0:len(ifile)-4] + '_temp.xml'
        command = 'odf2xml ' + '-o ' + tempfile + ' ' + ifile
        runShell(command)
        with open(tempfile, mode='r', encoding='utf-8') as f:
            data = f.read()
            replaced = []
            for i, letter in enumerate(data):
                if letter in ['\n', '\t', '\r']:
                    replaced.append([i, letter])
            data = data.replace('\n', ' ').replace(
                '\t', ' ').replace('\r', ' ')
        remove_file_command = 'rm ' + tempfile
        runShell(remove_file_command)
        return [data, replaced]


def find_entities(ifile,
                  ofile=None,
                  method=['strict', "*", "True"],
                  patterns_file='patterns.json',
                  verbose=False,
                  words_array=[],
                  remove_words=[],
                  quick=False):

    in_order = True

    # Create name for the output file
    # if not given by user
    if ofile == None:
        ofile = create_output_file_name(ifile=ifile)

    # Check file extension
    extension = ifile[-3:]
    if extension == 'odt':
        [data, replaced] = read_data_from_file(ifile=ifile,
                                               format='odt')
    elif extension == 'txt':
        [data, replaced] = read_data_from_file(ifile=ifile,
                                               format='txt')
    else:
        raise NameError('find_entities: Not extension .txt or .odt')
    # doc = nlp(data)
    # data = str(doc)

    # READ CONFIGURATION FILE
    #
    patterns_json = read_patterns(patterns_file)


    # Except whole parts from the text

    '''
    It is possible that some parts in the text have
    to stay untouched. Therefore, we should except
    these parts from the anonymizer.

    This function should create a list called
    EXCEPTED_PARTS containing lists of type:
    [start,end] for each excepted part.
    '''
    def except_parts(excepted_list=None):

        # If nothing is given return empty list
        if excepted_list == None:
            return []

        '''
        In order to remove some parts from anonymization
        we should first identify starting and ending spans
        id in text.
        After that we can except anything between these
        two parts.
        '''
        def find_part(rgx):
            import re
            results = []
            for match in re.finditer(rgx, data):
                s = match.start()
                e = match.end()
                span = data[s:e]
                if s==e :
                    continue
                return [s,e] #span removed
                ## NEEDS FIX TO FIND FIRST MATCH ONLY


        excepted_parts = []
        for rgx in excepted_list:
            value = find_part(rgx=rgx)
            if value != None:
                excepted_parts.append( value)
        return excepted_parts

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
    if not quick:
        # Do not do the whole search
        for matcher, value in patterns_json['matcher'].items():
            if value['active'] == 'False':
                continue
            custom_pattern_method = getattr(matcher_patterns, matcher)
            # Call function with the proper parameters
            results = custom_pattern_method(
                data=data, pattern=fix_patterns(value['pattern']))
            if results != None:
                entities += results

    # Words Array , Custom word search in text
    for word in words_array:
        [method_type,
         symbol,
         length_replace] = method
        if len(symbol) > 1:
            symbol = symbol[0]
        if symbol in word:
            # Make anonymize something like '9 **** 2019'
            # Semi-anionymized
            splitted_word = word.split(symbol)
            pattern = r''
            for item in splitted_word:
                # Find . (anything) instead of *
                pattern += item + '.'
            pattern = pattern[0:len(pattern)-1]

        else:
            pattern = word

        results = matcher_patterns.custom_words(data=data, word=pattern)
        if results != None:
            entities += results

    if in_order == True:
        entities.sort(key=sort_by_start)

    # Call except_parts here
    # All excepted regexes should be read from json file
    excepted_parts = except_parts([r'Συνεδρίασε\sδημόσια.*?Για\sνα\sδικάσει\s+|$'])

    excepted_rgx = []
    for part_id, rgx in patterns_json['excepted_parts'].items():
        excepted_rgx.append(fix_pattern(rgx))
    excepted_parts = except_parts(excepted_rgx)


    unique_values = True
    if unique_values == True:
        final_entities = []
        for entity in entities:
            if entity not in final_entities:
                final_entities.append(entity)
        entities = final_entities

    # Before finalizing the list except any parts
    # that should not be anonymized
    final_entities = []
    removed_spans = []
    for entity in entities:
        s = entity[3]
        e = entity[4]

        for [part_s,part_e] in excepted_parts:
            if s >= part_s and e <= part_e:
            # Entity exists within the part
            # Do not add it to final_entities
                removed_spans.append(entity[2])
            else:
                final_entities.append(entity)
    entities = final_entities

    # All removed_spans may be repeated in the text
    # therefore they should be removed everywhere
    if removed_spans != []:
        entities = [entity for entity in entities if entity[2] not in removed_spans]

    # Remove specific words added by user
    if remove_words != []:
        entities = [entity for entity in entities if entity[2]
                    not in remove_words]

    if verbose:
        # Display
        print(
            colored(f'\n\n-------------File:{ifile}-------------', 'green'))
        for element in entities:
            print('[', colored(element[0], 'yellow'), ',', colored(
                element[1], 'blue'), ',', colored(element[2], 'cyan'),
                ',', element[3], ',', element[4],
                ']',)

    # Anonymize entities by removing them
    # from the original file

    final_text = ''
    index = 0
    previous_e = 0
    for element in entities:
        span = element[2]
        s = element[3]
        e = element[4]
        # Brand elements may have html tags in .odt files
        if element[0] == 'brand_name' and ifile[-3:] == 'odt':
            final_text += data[index:s]
            index = s
            previous_e = e
            import re
            regex = r'(<.*?>)'
            tags = []
            for match in re.finditer(regex, span):
                st = match.start()
                end = match.end()
                sp = span[st:end]
                tags.append([st, end, sp])
            if tags == []:
                final_text += data[index:s] + \
                    anonymize_element(element, method)
                previous_e = e
                index = e
                continue
            temp_index = index
            for tag in tags:
                st = tag[0]
                end = tag[1]
                sp = tag[2]
                temp_data = data[temp_index:index+st]
                temp_element = [
                    'brand_name',
                    temp_data.upper(),
                    temp_data,
                    temp_index,
                    index+st,
                    False
                ]

                final_text += anonymize_element(temp_element, method)
                final_text += sp
                temp_index = index + end
            temp_data = data[temp_index:e]
            temp_element = [
                'brand_name',
                temp_data.upper(),
                temp_data,
                temp_index,
                e,
                False
            ]

            final_text += anonymize_element(temp_element, method)
            # index = previous_e
            # index = e
            index = e
            continue
        if previous_e >= e:
            # currenct element is substring of the previous
            index = previous_e
            continue
        elif (s >= previous_e):
            # Common case
            final_text += data[index:s] + anonymize_element(element, method)
            previous_e = e
            index = e
        else:
            # previous and current element have both a common substring
                # f'Weird case span_trimmed:{data[previous_e:e]},span:{span}')
            temp_element = [
                element[0],
                element[1],
                data[previous_e:e],
                previous_e,
                e,
                element[5]
            ]
            final_text += anonymize_element(
                temp_element, method)
            previous_e = e
            index = e
    if index < len(data):
        final_text += data[index:len(data)]

    # Get the original new lines
    for i, letter in replaced:
        final_text = final_text[:i] + letter + final_text[i+1:]

    with open(ofile, mode='w') as of:
        of.write(final_text)

    if ifile[-3:] == 'odt':
        # Create an odt file
        # Remove the file above
        command = 'xml2odf -o ' + ofile + ' ' + ofile
        runShell(command)
