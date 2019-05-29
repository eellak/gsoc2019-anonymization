def phone_number(matcher, handler=None):

    # +30 123123123
    # phone_number_pattern = [{"TEXT": {"REGEX": "^\+[\d]{2}[\d *]{10}"}}]
    phone_number_pattern = [{"TEXT": {
        "REGEX": r"(\+(\s)*[0-9]{2})*([\s|\.|-])*([0-9]{3})([\s|\.|-])*([0-9]{3})([\s|\.|-])*([0-9]{4})"}}]
    matcher.add("phone_number", handler, phone_number_pattern)

    greek_mobile_number_pattern = [{"TEXT": {
        "REGEX": r"(\+(\s)*30)*([\s|\.|-])*(69[0-9]{1})([\s|\.|-])*([0-9]{3})([\s|\.|-])*([0-9]{4})"}}]
    matcher.add("greek_mobile_number", handler, greek_mobile_number_pattern)

    greek_phone_number_pattern = [{"TEXT": {
        "REGEX": r"(\+(\s)*30)*([\s|\.|-])*(2[0-9]{2})([\s|\.|-])*([0-9]{3})([\s|\.|-])*([0-9]{4})"}}]
    matcher.add("greek_phone_number", handler, greek_phone_number_pattern)
