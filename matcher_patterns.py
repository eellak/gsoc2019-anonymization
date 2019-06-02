def phone_number(data, matcher=None, handler=None, regex=True):

    if regex:
        import re
        results = []
        general_phone_number_pattern = r'\b(\+[\s]*[0-9]{2})?[\s\.\-]*([0-9]{3})[\s\.\-]*([0-9]{3})[\s\.\-]*([0-9]{4})\b'
        greek_mobile_number_pattern = r'\b(\+[\s]*30)?[\s\.\-]*(69[0-9]{1})[\s\.\-]*([0-9]{3})[\s\.\-]*([0-9]{4})\b'
        greek_phone_number_pattern = r'\b(\+[\s]*30)?[\s\.\-]*(2[0-9]{2})[\s\.\-]*([0-9]{3})[\s\.\-]*([0-9]{4})\b'
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

        # print(span)
        # results.append([entity_name, span, s, e, found_by_spacy])

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


def vehicle(data, handler=None):
    import re
    # update: vehicle patterns only uppercase, case insensitive
    vehicle_pattern = r'\b((([ΑΒΕΖΗΙΚΜΝΟΡΤΥΧABEZHIKMNOPTYX])([\s.])?){3})([-\s])*([0-9]{4})\b'
    rare_vehicle_pattern = r'\b((([ΠΣ])[\s.]?){2})([-\s])*([0-9]{4})'
    '''security forces + construction machinery + farm machinery + trailers'''
    special_vehicle_pattern = r'\b(([ΠΣΕΑΛΡΜSEAMP][\s.]?){2})[-\s]*([0-9]{5})\b'
    ''' diplomatic corps'''
    diplomatic_corps_vehicle_pattern = r'\b(([ΔΣ][.\s]?){2})(([0-9][\s]?){2}[\s-]*[0-9]{1})[\s]?(CD[\s.]?|cd[\s.]?)\b'

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


def identity_card(data, handler=None):
    import re
    results = []
    identity_card_pattern = r'(?i)\s\b(([α-ω][\s.]?){2})[\s-]?(([0-9][\s]?){6})\b'
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


def iban(data, handler=None):
    import re
    results = []
    iban_pattern = r'(?i)\b(IBAN|iban|ΙΒΑΝ|ιβαν)([\s\-:]*)(([A-Z]|[a-z]){2}([\s\-]*\d){25})\b'
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


def afm(data, handler=None):
    import re
    results = []
    # afm_pattern = r'(?i)\bα[\s.]?φ[\s.]?μ[\s.]?[\s:]*([0-9]{9})\b'
    afm_pattern = r'(?i)\bα[\s.]?φ[\s.]?μ[\s.]?[\s\-]?[\w]*?[\s:]*([0-9]{9})\b'
    for match in re.finditer(afm_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'afm'
        entity_value = match.group(1)
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    return results


def amka(data, handler=None):
    import re
    results = []
    # amka_pattern = r'(?i)\b(α[\s.]?μ[\s.]?κ[\s.]?α[\s.]?)[\s.:](([012][0-9]|30|31)([0-9]|10|11|12)[0-9][0-9][0-9]{5})\b'
    amka_pattern = r'(?i)\b(α[\s.]?μ[\s.]?κ[\s.]?α[\s.]?)[\w]*?[\s.:](([012][0-9]|30|31)([0-9]|10|11|12)[0-9][0-9][0-9]{5})\b'
    for match in re.finditer(amka_pattern, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'amka'
        entity_value = match.group(2)
        found_by_spacy = False
        results.append([entity_name, entity_value, span, s, e, found_by_spacy])
    return results


def brand(data, handler=None):
    import re
    results = []
    brand_name_pattern = r'(?i)\b(επωνυμία|επωνυμια)[\s:]?«(.*?)»{1}'
    brand_distinctive_title_pattern = r'(?i)\b(διακριτικό|διακριτικο)[\s\-]?(τίτλο|τιτλο)[\s:]?«(.*?)»{1}'
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
