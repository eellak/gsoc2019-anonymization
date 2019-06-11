def create_output_file_name(ifile):
    extensions = ['.txt', '.odt']
    for extension in extensions:
        if extension in ifile:
            splitted = ifile.split(extension)
            outputfile = splitted[0] + '_anonymized' + extension
            return ifile
    raise NameError(f'{ifile} not found')
