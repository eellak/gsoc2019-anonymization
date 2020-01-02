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
            return outputfile
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


def fix_patterns(patterns):
    import json
    pattern = {}
    for key, value in patterns.items():
        value = value.replace('<#ec>', '\\')
        try:
            pattern.update({key: value})
        except:
            raise NameError(
                'Make sure that values in patterns.json patterns are different within each function')
    return(pattern)

def fix_pattern(rgx):
    return rgx.replace('<#ec>','\\')

def find_path(conf_file='anonymizer/conf.json', file_needed=None):
    import os

    if conf_file == None:
        raise NameError('find_path:No configuration file given')
    if file_needed == None:
        raise NameError('find_path:No file given')
    import json
    with open(conf_file, mode='r') as json_file:
        data = json.load(json_file)
    paths = data['paths']

    retval = os.path.dirname(os.path.abspath(
        __file__)) + '/' + paths[file_needed]
    return retval
