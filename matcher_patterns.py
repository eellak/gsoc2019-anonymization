def phone_number(matcher, data, handler=None, regex=True):

    if regex:
        import re
        results = []
        general_phone_number_pattern = r'(\+(\s)*[0-9]{2})*([\s\.-])*([0-9]{3})([\s\.-])*([0-9]{3})([\s\.-])*([0-9]{4})'
        greek_mobile_number_pattern = r'(\+(\s)*30)*([\s\.-])*(69[0-9]{1})([\s\.-])*([0-9]{3})([\s\.-])*([0-9]{4})'
        greek_phone_number_pattern = r'(\+(\s)*30)*([\s\.-])*(2[0-9]{2})([\s\.-])*([0-9]{3})([\s\.-])*([0-9]{4})'
        for match in re.finditer(greek_mobile_number_pattern, data):
            s = match.start()
            e = match.end()
            span = data[s:e]
            entity_name = 'greek_mobile_number'
            found_by_spacy = False
            results.append([entity_name, span, s, e, found_by_spacy])
        for match in re.finditer(greek_phone_number_pattern, data):
            s = match.start()
            e = match.end()
            span = data[s:e]
            entity_name = 'greek_phone_number'
            found_by_spacy = False
            results.append([entity_name, span, s, e, found_by_spacy])
        for match in re.finditer(general_phone_number_pattern, data):
            s = match.start()
            e = match.end()
            span = data[s:e]
            entity_name = 'general_phone_number'
            found_by_spacy = False
            temp = True
            for i, _ in enumerate(results):
                if span in results[i]:
                    temp = False
                    break
            if temp:
                results.append([entity_name, span, s, e, found_by_spacy])

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


def vehicles(data, handler=None):
    import re
    vehicle_regex = r'(?i)(\b(([αβεζηικμνορτυχabezhikmnoptyx]([\s.])?){3})([-\s])*([0-9]{4}))'
    rare_vehicles1 = r'(?i)(\b(([πσ])([\s.])?){2}([-\s])*([0-9]{4}))'
    '''security forces + construction machinery + farm machinery + trailers'''
    special_vehicle = r'(?i)([πσεαλρμseamp])([\s.]?){2}([-\s])*([0-9]{5})'
    ''' diplomatic corps'''
    diplomatic_corps_vehicle = r'(?i)(([δσ][.\s]?){2}([0-9][\s]?){2})([\s-]?)([0-9]{1})'

    # ALTERNATIVE
    # matches = re.findall(vehicle_regex, data)
    results = []
    for match in re.finditer(vehicle_regex, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'vehicle'
        found_by_spacy = False
        results.append([entity_name, span, s, e, found_by_spacy])
    for match in re.finditer(rare_vehicles1, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'rare_vehicle'
        found_by_spacy = False
        results.append([entity_name, span, s, e, found_by_spacy])
    for match in re.finditer(special_vehicle, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'special_vehicle'
        found_by_spacy = False
        results.append([entity_name, span, s, e, found_by_spacy])
    for match in re.finditer(diplomatic_corps_vehicle, data):
        s = match.start()
        e = match.end()
        span = data[s:e]
        entity_name = 'diplomatic_corps_vehicle'
        found_by_spacy = False
        results.append([entity_name, span, s, e, found_by_spacy])

    return results
