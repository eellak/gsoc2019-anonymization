def sort_by_start(result=None):

    if result == None:
        return None
    return result[3]


def create_output_file_name(ifile):
    extensions = ['.txt', '.odt']
    for extension in extensions:
        if extension in ifile:
            splitted = ifile.split(extension)
            outputfile = splitted[0] + '_anonymized' + extension
            return ifile
    raise NameError(f'{ifile} not found')


def official_json(ifile):
    import json
    while '\\' in ifile:
        ifile = ifile.replace('\\', '<#ec>')
    jsonfile = json.loads(ifile)
    return jsonfile

    # filename = 'conf_temp.json'
    # with open(filename, 'w') as tmp:
    #     json.dumps(ifile)
    #     jsonfile = json.loads(ifile)


def fix_pattern(patterns):
    import json
    pattern = {}
    for key, value in patterns.items():
        value = value.replace('<#ec>', '\\')
        try:
            pattern.update({key: value})
        except:
            raise NameError(
                'Make sure that values in conf.json patterns are different within each function')
    return(pattern)
