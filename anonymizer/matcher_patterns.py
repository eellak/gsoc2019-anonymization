def phone_number(data, pattern=None, handler=None, regex=True, matcher=None):

    if regex == True:
        import re
        results = []
        if pattern == None:
            return []

        general_phone_number_pattern = pattern['general_phone_number_pattern']
        greek_mobile_number_pattern = pattern['greek_mobile_number_pattern']
        greek_phone_number_pattern = pattern['greek_phone_number_pattern']

        for match in re.finditer(greek_mobile_number_pattern, data):
            s = match.start()
            e = match.end()
            span = data[s:e]
            entity_name = 'greek_mobile_number'
            entity_value = (match.group(1) if match.group(
                1) != None else '') + match.group(2) + match.group(3) + match.group(4)
            found_by_spacy = False
            results.append([entity_name, entity_value,
                            span, s, e, found_by_spacy])
        for match in re.finditer(greek_phone_number_pattern, data):
            s = match.start()
            e = match.end()
            span = data[s:e]
            entity_name = 'greek_phone_number'
            entity_value = (match.group(1) if match.group(
                1) != None else '') + match.group(2) + match.group(3) + match.group(4)
            found_by_spacy = False
            results.append([entity_name, entity_value,
                            span, s, e, found_by_spacy])
        for match in re.finditer(general_phone_number_pattern, data):
            s = match.start()
            e = match.end()
            span = data[s:e]
            entity_name = 'general_phone_number'
            entity_value = (match.group(1) if match.group(1)
                            != None else '') + match.group(2) + match.group(3) + match.group(4)
            found_by_spacy = False
            temp = True
            for i, _ in enumerate(results):
                if span in results[i]:
                    temp = False
                    break
            if temp:
                results.append([entity_name, entity_value,
                                span, s, e, found_by_spacy])

        return results

    else:
        # +30 123123123
        # phone_number_pattern = [{"TEXT": {"REGEX": "^\+[\d]{2}[\d *]{10}"}}]
        phone_number_pattern = [{"TEXT": {
            "REGEX": r"(\+(\s)*[0-9]{2})*([\s\.-])*([0-9]{3})([\s\.-])*([0-9]{3})([\s\.-])*([0-9]{4})"}}]
        matcher.add("phone_number", handler, phone_number_pattern)

        greek_mobile_number_pattern = [{"TEXT": {
            "REGEX": r"(\+(\s)*30)*([\s\.-])*(69[0-9]{1})([\s\.-])*([0-9]{3})([\s\.-])*([0-9]{4})"}}]
        matcher.add("greek_mobile_number", handler,
                    greek_mobile_number_pattern)

        greek_phone_number_pattern = [{"TEXT": {
            "REGEX": r"(\+(\s)*30)*([\s\.-])*(2[0-9]{2})([\s\.-])*([0-9]{3})([\s\.-])*([0-9]{4})"}}]
        matcher.add("greek_phone_number", handler, greek_phone_number_pattern)


# REGEX -- due to spacy issue with spaces in regex


def vehicle(data, pattern=None, handler=None):
    import re

    if pattern == None:
        return []

    # update: vehicle patterns only uppercase, case insensitive
    vehicle_pattern = pattern['vehicle_pattern']
    rare_vehicle_pattern = pattern['rare_vehicle_pattern']
    '''security forces + construction machinery + farm machinery + trailers'''
    special_vehicle_pattern = pattern['special_vehicle_pattern']
    ''' diplomatic corps'''
    diplomatic_corps_vehicle_pattern = pattern['diplomatic_corps_vehicle_pattern']

    results = []

    for match in re.finditer(vehicle_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'vehicle'
        entity_value = match.group(1).strip().replace(
            '.', '') + '-' + match.group(6).strip()
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    for match in re.finditer(rare_vehicle_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'rare_vehicle'
        entity_value = match.group(1).strip().replace(
            '.', '') + '-' + match.group(5).strip()
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    for match in re.finditer(special_vehicle_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'special_vehicle'
        entity_value = match.group(1).strip().replace(
            '.', '') + '-' + match.group(3).strip()
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    for match in re.finditer(diplomatic_corps_vehicle_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'diplomatic_corps_vehicle'
        entity_value = match.group(1).strip().replace(
            '.', '') + '-' + match.group(3).replace('-', '') + '-' + match.group(5).strip().replace('.', '')
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])

    return results


def identity_card(data, pattern=None, handler=None):
    import re
    results = []
    if pattern == None:
        return []
    identity_card_pattern = pattern['identity_card_pattern']
    for match in re.finditer(identity_card_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'identity_card'
        entity_value = match.group(1).replace(
            ' ', '') + '-' + match.group(3).strip().replace(' ', '')
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    return results


def iban(data, pattern=None, handler=None):
    import re
    results = []
    if pattern == None:
        return []
    iban_pattern = pattern['iban_pattern']
    for match in re.finditer(iban_pattern, data):
        # Make sure it is a correct iban
        # example: iban GR-16-01101250000000012300675 -->
        # group(0) whole prase
        # group(1) 'iban'
        # group(2) ' '
        # group(3) 'GR-16-01101250000000012300675'
        iban_number = match.group(3)
        iban_number = iban_number.replace('\n', ' ')
        iban_number = iban_number.replace('\t', ' ')
        iban_number = iban_number.replace('\r', ' ')
        iban_number = iban_number.replace('\f', ' ')
        iban_number = iban_number.replace('-', '')
        iban_number = iban_number.replace(' ', '')
        if len(iban_number) != 27:
            raise NameError('WRONG IBAN')
        else:
            first_part = iban_number[0:4]
            second_part = iban_number[4:27]
            converted_iban = second_part+first_part
            from string import ascii_uppercase as a_up
            final_iban = []
            for letter in converted_iban:
                if letter in a_up:
                    letter_number = a_up.index(letter) + 10
                    final_iban += (str(letter_number))
                else:
                    final_iban += letter
            final_iban = int(''.join(final_iban))
            [_, mod] = divmod(final_iban, 97)
            if mod == 1:
                # Correct iban according to
                # https://en.wikipedia.org/wiki/International_Bank_Account_Number

                s = match.start()
                e = match.end()
                span = data[s:e]
                entity_name = 'iban'
                entity_value = iban_number
                found_by_spacy = False
                results.append([entity_name, entity_value,
                                span, s, e, found_by_spacy])
    return results


def afm(data, pattern=None, handler=None):
    import re
    results = []
    if pattern == None:
        return []
    # afm_pattern = r'(?i)\bα[\s.]?φ[\s.]?μ[\s.]?[\s:]*([0-9]{9})\b'
    afm_pattern = pattern['afm_pattern']
    for match in re.finditer(afm_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'afm'
        entity_value = match.group(1)
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    return results


def amka(data, pattern=None, handler=None):
    import re
    results = []
    if pattern == None:
        return []
    amka_pattern = pattern['amka_pattern']
    for match in re.finditer(amka_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'amka'
        entity_value = match.group(2)
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    return results


def brand(data, pattern=None, handler=None):
    import re
    results = []
    if pattern == None:
        return []
    brand_name_pattern = pattern['brand_name_pattern']
    brand_distinctive_title_pattern = pattern['brand_distinctive_title_pattern']
    for match in re.finditer(brand_name_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'brand_name'
        entity_value = match.group(2).upper()
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    for match in re.finditer(brand_distinctive_title_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'brand_distinctive_title'
        entity_value = match.group(3).upper()
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    return results


def address(data, pattern=None, handler=None):
    import re
    if pattern == None:
        return []
    results = []
    # address_pattern = r'(?i)\b(?:οδός|οδος|οδο|οδό|οδού|οδου)[\s:]+?(.+?)[,\s]+?((?:αρ)[ιί]?[θ]?[μ]?[οό]?[υύ]?[\.]?[:]?[\s]?(.+?\b))?'
    # better approach: Addresses start with uppercase letters
    # address_pattern = pattern['address_pattern']
    # multiple_address_pattern = (r'\b(?:οδών|οδων|Οδών|Οδων)[\s:]+?' +
    #                             r'(?P<address1>(?:[Α-Ω]\w*.?\s?)+?)[,\s]+?(?:με\s)?((?:αρ)[ιί]?[θ]?[μ]?[οό]?[υύ]?[\.]?[:]?[\s]?(?P<number1>.+?\b))' +
    #                             r'(?:[\w]?[\s,]*(?:και|Και|κι)[\s,]*)' +
    #                             r'(?P<address2>(?:[Α-Ω]\w*.?\s?)+?)[,\s]+?(?:με\s)?((?:αρ)[ιί]?[θ]?[μ]?[οό]?[υύ]?[\.]?[:]?[\s]?(?P<number2>.+?\b))')
    address_pattern = pattern['address_pattern']
    multiple_address_pattern = pattern['multiple_address_pattern']
    for match in re.finditer(address_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'address'
        entity_value = match.group('address').strip(
        ).replace(',', '') + ('-' + match.group('number').strip() if match.group('number') != None else '')
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    for match in re.finditer(multiple_address_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'multiple_addresses'
        entity_value = [
            match.group('address1').strip().replace(',', '') +
            ('-' + match.group('number1').strip()
             if match.group('number1') != None else ''),

            match.group('address2').strip().replace(',', '') +
            ('-' + match.group('number2').strip()
             if match.group('number1') != None else '')
        ]
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    
    return results

def known_address(data,pattern=None):

    if pattern==[]:
        return []
    results = []

    import re
    from anonymizer.trie_index import create_trie_index
    from anonymizer.trie_index import prepair_word
    import os 
    known_addresses = pattern['known_address_pattern']
    # Create dataset
    cwd = os.path.dirname(os.path.abspath(__file__))
    dataset = cwd + '/data/odoi.csv'
    # dataset = 'anonymizer/data/odoi.csv'
    address_trie_index = create_trie_index(dataset=dataset)
    for match in re.finditer(known_addresses,data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        word_to_search = span.replace(' ', '_').replace('-', '_')
        # Search this matched pattern in trie index
        if address_trie_index.search(prepair_word(word_to_search)) == 1:
            results.append([
                'address',
                span.upper(),
                span,
                s,
                e,
                False
            ])
    

    return results


def name(data, pattern=None, handler=None, strict_surname_matcher=True):
    if pattern == None:
        return []
    from anonymizer import trie_index
    from anonymizer.trie_index import prepair_word
    import re
    results = []
    possible_names = []
    starts = []
    ends = []
    not_final_results = []
    name_pattern = pattern['name_pattern']
    for match in re.finditer(name_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        possible_names.append(span)
        entity_name = 'name'
        entity_value = span.upper()
        found_by_spacy = False
        not_final_results.append([
            entity_name,
            entity_value,
            span,
            s,
            e,
            found_by_spacy
        ])
    import os
    cwd = os.path.dirname(os.path.abspath(__file__))
    name_trie_index = trie_index.create_trie_index_for_names(
        cwd + '/data/male_and_female_names.txt')

    # Possible names. Words that start with uppercase letter
    are_names = []
    for word in possible_names:
        # Search for different keys
        if name_trie_index.search(prepair_word(word=word)) == 1:
            # word is found
            are_names.append(True)

        else:
            are_names.append(False)

    for index, is_name in enumerate(are_names):
        if is_name == True:
            results.append(not_final_results[index])

    # Now fine surnames that maybe exist for each name in list
    #

    surnames = []
    names = [result[2] for result in results]
    name_set = set(names)
    names = list(name_set)

    surnames_postfixes = ['ιατης', 'ιατη', 'αιτης', 'αιτη',
                          'ιδης', 'ιδη', 'αδης', 'αδη',
                          'ογλου', 'ακος', 'ακου', 'ακης',
                          'ακη', 'πουλος', 'πουλου', 'νος',
                          'αιος', 'λας', 'ιου', 'ιδης',
                          'ουλας', 'κος', 'αρης', 'εας',
                          'αιας', 'αια', 'ουρας', 'ουρα',
                          'ινας', 'ινης', 'ινη', 'μης',
                          'μη', 'ονους', 'ονου', 'ιωτης',
                          'ιωτη', 'ιτης', 'ιτη', 'ιανος',
                          'ιανου', 'ιανη', 'ινος', 'ινου',
                          'αιου', 'λα', 'νου',
                          ]

    surnames_postfixes = [
        'ος', 'ου', 'ης', 'η', 'ους', 'ας', 'α'
    ]

    # Safewords:
    # These words will never be parsed as surnames
    #
    from anonymizer.external_functions import find_path
    cwd = os.path.dirname(os.path.abspath(__file__))
    safewords_path = find_path( (cwd+'/conf.json'), 'safewords')
    print(safewords_path)
    with open(safewords_path, mode='r') as sw:
        safe_words = [word.replace('\n', '') for word in sw.readlines()]

    for index, name in enumerate(names):
        if prepair_word(name) in safe_words:
            try:
                # print(f'I found {prepair_word(name)} in names')
                names.remove(name)
            except:
                raise NameError(f'Can not remove {name}')
            continue
        # surname_pattern = (r'(?P<possible_surname_before>\b[Α-ΩΆΈΌΊΏΉΎ]+[α-ωάέόίώήύ]*\b)?' +
        #                    r'[\s]?' +
        #                    name +
        #                    r'[\s]?' +
        #                    r'(?P<possible_surname_after>\b[Α-ΩΆΈΌΊΏΉΎ]+[α-ωάέόίώήύ]*\b)?')

        surname_pattern = pattern['surname_pattern_before'] + \
            name + pattern['surname_pattern_after']
        for match in re.finditer(surname_pattern, data):
            possible_surname_before = match.group('possible_surname_before')
            possible_surname_after = match.group('possible_surname_after')
            if possible_surname_before != None:
                if prepair_word(possible_surname_before) in safe_words:
                    # print(possible_surname_before)
                    len_surname_before = len(possible_surname_before)
                    possible_surname_before = None
            if possible_surname_after != None:
                if prepair_word(possible_surname_after) in safe_words:
                    # print(possible_surname_after)
                    len_surname_after = len(possible_surname_after)
                    possible_surname_after = None

            if (possible_surname_before == None and possible_surname_after != None):

                if strict_surname_matcher == False:
                    s = match.start()
                    e = match.end()
                    span = data[s:e]
                    surname = possible_surname_after
                    fullname = name + ' ' + surname
                    results[index][0] = ('name-surname')
                    results[index][1] = (name + '-' + surname).upper().strip()
                    results[index][2] = span
                    results[index][3] = s
                    results[index][4] = e

                else:
                    #  Logical value to check if it is indeed surname after loop
                    #  for each different postfix
                    is_surname_strict = False

                    for surname_postfix in surnames_postfixes:
                        l = len(surname_postfix)
                        sur_l = len(possible_surname_after)
                        if (sur_l < l):
                            continue

                        to_be_compared = prepair_word(
                            possible_surname_after[sur_l-l:sur_l])

                        if (to_be_compared == surname_postfix):
                            # Strict match of surname
                            #
                            is_surname_strict = True
                            break

                    if is_surname_strict == True:
                        # Now we know it is surname
                        # So pass the value to results
                        surname = possible_surname_after
                        # s = (match.start() + len_surname_before if possible_surname_before==None else match.start())
                        s = match.start()
                        e = match.end()
                        span = data[s:e]
                        s1 = span.index(name)
                        s = s + s1
                        span = data[s:e]

                        # s = span.index(name)
                        # e = span.index(surname) + len(surname)
                        # span = span[s:e]
                        results[index][0] = ('name-surname-after')
                        results[index][1] = (
                            name + '-' + surname).upper().strip()
                        results[index][2] = span
                        results[index][3] = s
                        results[index][4] = e

            elif (possible_surname_before != None and possible_surname_after == None):

                if strict_surname_matcher == False:
                    s = match.start()
                    e = match.end()
                    span = data[s:e]
                    end_name_index = span.index(name)
                    e = s + end_name_index
                    span = data[s:e]
                    surname = possible_surname_before
                    fullname = name + ' ' + surname
                    results[index][0] = ('name-surname-before')
                    results[index][1] = (name + '-' + surname).upper().strip()
                    results[index][2] = span
                    results[index][3] = s
                    results[index][4] = e
                else:
                    #  Logical value to check if it is indeed surname before loop
                    #  for each different postfix
                    is_surname_strict = False

                    for surname_postfix in surnames_postfixes:
                        l = len(surname_postfix)
                        sur_l = len(possible_surname_before)
                        if (sur_l < l):
                            continue
                        to_be_compared = prepair_word(
                            possible_surname_before[sur_l-l:sur_l])

                        if (to_be_compared == surname_postfix):
                            # Strict match of surname
                            #
                            is_surname_strict = True
                            break

                    if is_surname_strict == True:
                        # Now we know it is surname
                        # So pass the value to results
                        surname = possible_surname_before
                        s = match.start()
                        e = match.end()
                        span = data[s:e]
                        results[index][0] = ('name-surname')
                        results[index][1] = (
                            name + '-' + surname).upper().strip()
                        results[index][2] = span
                        results[index][3] = s
                        results[index][4] = e

            elif (possible_surname_before != None and possible_surname_after != None):

                if strict_surname_matcher == False:
                    s = match.start()
                    e = match.end()
                    span = data[s:e]
                    results[index][0] = ('name-surname')
                    results[index][1] = (name + '-' +
                                         possible_surname_before + '-' +
                                         possible_surname_after
                                         ).upper().strip()
                    results[index][2] = span
                    results[index][3] = s
                    results[index][4] = e
                else:
                    #  Logical values to check if it is indeed surname before loop
                    #  for each different postfix.
                    #  One for the surname to the left and one for the right.
                    #  We check them both and decide

                    is_surname_strict_before = False
                    is_surname_strict_after = False
                    surname_before = None
                    surname_after = None

                    for surname_postfix in surnames_postfixes:
                        l = len(surname_postfix)
                        sur_l = len(possible_surname_before)
                        if (sur_l < l):
                            continue
                        to_be_compared = prepair_word(
                            possible_surname_before[sur_l-l:sur_l])

                        if (to_be_compared == surname_postfix):
                            # Strict match of surname
                            #
                            is_surname_strict_before = True
                            break

                    if is_surname_strict_before == True:
                        # Now we know it is surname the one before
                        # So pass the value to results
                        surname_before = possible_surname_before

                    for surname_postfix in surnames_postfixes:
                        l = len(surname_postfix)
                        sur_l = len(possible_surname_after)
                        if (sur_l < l):
                            continue
                        to_be_compared = possible_surname_after[sur_l-l:sur_l].lower(
                        )

                        if (to_be_compared == surname_postfix):
                            # Strict match of surname
                            #
                            is_surname_strict_after = True
                            break

                    if is_surname_strict_after == True:
                        # Now we know it is surname
                        # So pass the value to results
                        surname_after = possible_surname_after

                    # Initialize s,e,span for results to be returned
                    s = match.start()
                    e = match.end()
                    span = data[s:e]

                    # Choose the final result
                    if surname_before == None and surname_after != None:
                        surname = surname_after
                        # change the start in span
                        s = s + span.index(surname_after)
                        span = data[s:e]

                    elif surname_before != None and surname_after == None:
                        surname = surname_before
                        # change the end in span
                        e = s + span.index(name) + len(name)
                        span = data[s:e]

                    elif surname_before != None and surname_after != None:
                        surname = surname_before + '-' + surname_after
                    else:
                        surname = None
                        continue

                    results[index][0] = ('name-surname')
                    results[index][1] = (
                        name + '-' + surname).upper().strip()
                    results[index][2] = span
                    results[index][3] = s
                    results[index][4] = e

    # Mr surname or Miss Surname identified down below:
    #

    surname_pattern_mr = pattern['surname_pattern_mr']

    for match in re.finditer(surname_pattern_mr, data):
        entity_value = match.group('surname').strip()
        # Check if the entity value is surname
        if prepair_word(entity_value) in safe_words:
            continue
        is_surname = False
        for postfix in surnames_postfixes:
            postfix_len = len(postfix)
            entity_value_len = len(entity_value)
            if entity_value_len < postfix_len:
                continue
            if prepair_word(entity_value[entity_value_len-postfix_len:entity_value_len]) == postfix:
                is_surname = True
                break
        # If not surname go to the next iteration
        if is_surname == False:
            continue

        # Here we know it is surname
        #
        entity_value = entity_value.upper()
        s = match.start()
        e = match.end()
        span = data[s:e]
        results.append(['surname', entity_value, span, s, e, False])

    surname_pattern_with_prefix = pattern['surname_pattern_with_prefix']
    # [^.Α-Ωα-ω]
    for match in re.finditer(surname_pattern_with_prefix, data):
        entity_value = match.group('surname').strip()
        if prepair_word(entity_value) in safe_words:
            continue
        # Check if the entity value is surname
        is_surname = False
        for postfix in surnames_postfixes:
            postfix_len = len(postfix)
            entity_value_len = len(entity_value)
            if entity_value_len < postfix_len:
                continue
            if prepair_word(entity_value[entity_value_len-postfix_len:entity_value_len]) == postfix:
                is_surname = True
                break
        # If not surname go to the next iteration
        if is_surname == False:
            continue

        # Here we know it is surname
        #
        entity_value = match.group('prefix').strip(
        ) + ' ' + match.group('surname').strip()
        entity_value = entity_value.upper()
        s = match.start()
        e = match.end()
        span = data[s:e]
        results.append(['name-surname', entity_value, span, s, e, False])

    middlename_pattern = pattern['middlename_pattern']
    for index, name in enumerate(names):
    
        # pattern contains already found name!
        surname_with_middlename_pattern = name + middlename_pattern
        for match in re.finditer(surname_with_middlename_pattern, data):
            s = match.start()
            e = match.end()
            span = data[s:e]
            surname = match.group('surname')
            middlename = match.group('middlename')
            surname_in_safewords = prepair_word(
                surname.replace('.', '')) in safe_words
            middlename_in_safewords = prepair_word(
                middlename.replace('.', '')) in safe_words

            if match.group('middlename') != None:
                if middlename_in_safewords:
                # This span is perhaps name so name matcher will catch it 
                    continue
            if surname != None and middlename != None:
                if surname_in_safewords:
                    # Update span
                    start_of_surname = span.index(surname)
                    e = s + start_of_surname
                    span = data[s:e]
                    
            entity_value = span.strip().replace(',','').upper()
            entity_name = 'name-middlename-surname'
            results.append([entity_name,entity_value,span,s,e,False])

    return results


def place(data, pattern=None, handler=None):

    import re
    import os
    from anonymizer.trie_index import create_trie_index
    from anonymizer.trie_index import prepair_word

    if pattern == None:
        return []

    # Create trie index first
    #
    # Both have no spaces
    # Nomoi dataset
    cwd = os.path.dirname(os.path.abspath(__file__))
    dataset = cwd + '/data/nomoi.csv'

    # dataset = 'anonymizer/data/nomoi.csv'
    place_trie_index_nomoi = create_trie_index(dataset=dataset)
    # Dhmoi dataset
    dataset = cwd + '/data/dhmoi.csv'

    # dataset = 'anonymizer/data/dhmoi.csv'
    place_trie_index_dhmoi = create_trie_index(dataset=dataset)

    # Find possible nomous using regex.
    place_pattern = pattern['place_pattern']

    results = []

    for match in re.finditer(place_pattern, data):

        s = match.start()
        e = match.end()
        span = data[s:e]

        if place_trie_index_nomoi.search(prepair_word(span)) == 1:
                # place is found in try index
            results.append([
                'place-nomos',
                span.upper(),
                span,
                s,
                e,
                False
            ])

        if place_trie_index_dhmoi.search(prepair_word(span)) == 1:
            # place is found in try index
            results.append([
                'place-nomos',
                span.upper(),
                span,
                s,
                e,
                False
            ])

    # Create dataset
    # This dataset - trie index handles any of: - or spaces as _

    # dataset = 'anonymizer/data/dioikhtikh_perifereia.csv'
    dataset = cwd + '/data/dioikhtikh_perifereia.csv'
    place_trie_index_periferia = create_trie_index(dataset=dataset)

    place_with_space_pattern = pattern['place_with_space_pattern']

    for match in re.finditer(place_with_space_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]

        word_to_search = span.replace(' ', '_').replace('-', '_')

        # First search for the max string

        if place_trie_index_periferia.search(prepair_word(word_to_search), print_index=False) == 1:
            # Add the place to the results
            results.append([
                'place-perifereia',
                span.upper(),
                span,
                s,
                e,
                False
            ])

        word1 = match.group('word1')
        word2 = match.group('word2')
        word3 = match.group('word3')
        # Then search for subgroup of possible perifereies (word1_word2 in regex)

        if word1 != None and word2 != None:
            word_to_search = word1.strip() + '_' + word2.strip()
            if place_trie_index_periferia.search(prepair_word(word_to_search)) == 1:
                # Add the place to the results
                s = data.index(word1.strip())
                e = data.index(word2.strip()) + len(word2.strip())
                span = data[s:e]
                results.append([
                    'place-perifereia',
                    word_to_search.upper(),
                    span,
                    s,
                    e,
                    False
                ])

        if word2 != None and word3 != None:
            word_to_search = word2.strip() + '_' + word3.strip()
            if place_trie_index_periferia.search(prepair_word(word_to_search)) == 1:
                # Add the place to the results
                s = data.index(word2.strip())
                e = data.index(word3.strip()) + len(word3.strip())
                span = data[s:e]
                results.append([
                    'place-perifereia',
                    word_to_search.upper(),
                    span,
                    s,
                    e,
                    False
                ])

        # Then search (if not None) each word as individual
        if word1 != None and (word2 != None or word3 != None):
            word_to_search = word1.strip()
            if place_trie_index_periferia.search(prepair_word(word_to_search)) == 1:
                # Add the place to the results
                e = s + len(word1.strip())
                span = data[s:e]
                results.append([
                    'place-perifereia',
                    word_to_search.upper(),
                    span,
                    s,
                    e,
                    False
                ])

        if word2 != None:

            word_to_search = word2.strip()
            if place_trie_index_periferia.search(prepair_word(word_to_search)) == 1:
                # Add the place to the results
                s = data.index(word2.strip())
                e = s + len(word2.strip())
                span = data[s:e]
                results.append([
                    'place-perifereia',
                    word_to_search.upper(),
                    span,
                    s,
                    e,
                    False
                ])
        if word3 != None:

            word_to_search = word3.strip()
            if place_trie_index_periferia.search(prepair_word(word_to_search)) == 1:
                # Add the place to the results
                s = data.index(word3.strip())
                e = s + len(word3.strip())
                span = data[s:e]
                results.append([
                    'place-perifereia',
                    word_to_search.upper(),
                    span,
                    s,
                    e,
                    False
                ])
    return results


def decision_number(data, pattern=None, handler=None):
    
    import re
    results = []
    
    decision_number_pattern = pattern['decision_number_pattern']
    for match in re.finditer(decision_number_pattern,data):
        s = match.start()
        e= match.end()
        span = data[s:e]
        results.append(['decision_number',span.upper(),span,s,e,False])

    return results

def custom_regex(data,pattern=None,handler=None):
    import re
    results = []
    for item in pattern:
        custom_regex_pattern = pattern[item]
        for match in re.finditer(custom_regex_pattern, data):
            s = match.start()
            e = match.end()
            span = data[s:e]
            results.append([item, span.upper(), span, s, e, False])
    return results

def custom_words(data,word=None,handler=None):

    import re 
    results = []
    for match in re.finditer(word.replace('"', ''), data):
        s = match.start()
        e= match.end()
        span = data[s:e]
        results.append(['custom_word',span.upper(),span,s,e,False])
    return results


