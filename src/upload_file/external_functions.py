import os
from os import system as runShell
from upload_file.models import Document


def anonymize_file(id='', user_folder='default', files_folder='files', custom_words='', text='', download=False, updateTextIfPossible=False):

    obj_file = Document.objects.get(id=id)
    filename = str(obj_file)
    file = os.path.join(os.path.dirname(__file__),
                        'documents/' + user_folder + '/' + files_folder + '/' + filename)
    directory = os.path.dirname(__file__)
    command = 'cd ' + directory
    runShell(command)
    command = 'cd ..'
    runShell(command)
    file_type = filename[-3:]

    if file_type == 'odt':

        file_name = filename
        l = len(file_name)
        anonymized_file_name = file_name[0:(
            l-4)] + '_anonymized' + file_name[(l-4):l]
        anonymized_file = os.path.join(os.path.dirname(__file__),
                                       'documents/' + user_folder + '/' + anonymized_file_name)

        # Convert odt to text just to preview
        # text = ///
        file_error = False
        anonymized_document_name = file_name[0:len(
            file_name)-4] + '_anonymized.odt'
        if download == False:
            # Preview the txt file
            tempname = 'temp_' + file_name[0:len(file_name)-4] + '.txt'
            temp_file = os.path.join(os.path.dirname(__file__),
                                     'documents/' + user_folder + '/' + tempname)

            # Check if file exists already or force update
            if not os.path.isfile(temp_file) or updateTextIfPossible:
                command = 'odt2txt ' + file + ' --output=' + temp_file
                runShell(command)

            custom_words_option = (
                " -w '" + custom_words + "'") if custom_words != '' else ''

            anonymized_file_name = tempname[0:(
                len(tempname)-4)] + '_anonymized.txt'
            anonymized_file = os.path.join(os.path.dirname(__file__),
                                           'documents/' + user_folder + '/' + anonymized_file_name)

            # Check if file exists already or force update
            if not os.path.isfile(anonymized_file) or updateTextIfPossible:
                command = ('python3 -m anonymizer_service' +
                           ' -i upload_file/documents/' + user_folder + '/' + tempname +
                           custom_words_option)
                runShell(command)

            with open(temp_file, mode='r') as f:
                text = f.read()
            # Always anonymize
            with open(anonymized_file, mode='r') as f:
                text_anonymized = f.read()
        else:
            custom_words_option = (
                " -w '" + custom_words + "'") if custom_words != '' else ''
            command = ('python3 -m anonymizer_service' +
                       ' -i ' + file +
                       ' -o ' + 'upload_file/documents/' + user_folder + '/' + anonymized_document_name +
                       custom_words_option)
            runShell(command)
            print('---------------------------------------------------')

            anonymized_file_name = file_name[0:(
                len(file_name)-4)] + '_anonymized.txt'
            anonymized_file = os.path.join(os.path.dirname(__file__),
                                           'documents/' + user_folder + '/' + anonymized_file_name)
            text = ''
            text_anonymized = ''
            return [{}, {}]

    elif file_type == 'txt':
        text = Document.objects.filter(id=1)
        file_name = filename
        l = len(file_name)
        anonymized_file_name = file_name[0:(
            l-4)] + '_anonymized' + file_name[(l-4):l]
        anonymized_file = os.path.join(os.path.dirname(__file__),
                                       'documents/' + user_folder + '/' + anonymized_file_name)

        # Check if file exists already or force update
        if not os.path.isfile(anonymized_file) or updateTextIfPossible:
            print('den to eixa')
            command = ('python3 -m anonymizer_service -i ' + file +
                       ' -o upload_file/documents/' + user_folder + '/' + anonymized_file_name + " -w '" + custom_words + "'")
            runShell(command)

        with open(file, mode='r') as f:
            text = f.read()
        with open(anonymized_file, mode='r') as f:
            text_anonymized = f.read()
        file_error = False
        anonymized_document_name = anonymized_file_name
    else:
        text = 'This file can not be supported.'
        file_error = True
        anonymized_document_name = 'FAILED'
        text_anonymized = ''

    document = {
        'name': filename,
        'text': text,
        'type': file_type,
        'user_folder': user_folder,
        'files_folder': files_folder,
        'error': file_error
    }

    document_anonymized = {
        'name': anonymized_document_name,
        'text': text_anonymized,
        'type': file_type,
        'user_folder': user_folder,
        'files_folder': files_folder,
        'error': file_error
    }

    return [document, document_anonymized]
