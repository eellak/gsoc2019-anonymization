import os
from os import system as runShell
from upload_file.models import Document


def anonymize_file(id='', user_folder='default', files_folder='files', custom_words=''):

    obj_file = Document.objects.get(id=id)
    filename = str(obj_file)
    file = os.path.join(os.path.dirname(__file__),
                        'documents/' + user_folder + files_folder + filename)
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
                                       'documents/' + user_folder + anonymized_file_name)

        # Convert odt to text just to preview
        # text = ///
        file_error = False
        tempname = 'temp_' + file_name[0:len(file_name)-4] + '.txt'
        temp_file = os.path.join(os.path.dirname(__file__),
                                 'documents/' + user_folder + tempname)

        command = 'odt2txt ' + file + ' --output=' + temp_file
        runShell(command)
        command = ('python3 -m anonymizer_service -i upload_file/documents/' + user_folder +
                   tempname + " -w '" + custom_words + "'")
        runShell(command)

        anonymized_file_name = tempname[0:(
            len(tempname)-4)] + '_anonymized.txt'
        anonymized_file = os.path.join(os.path.dirname(__file__),
                                       'documents/' + user_folder + anonymized_file_name)

        with open(temp_file, mode='r') as f:
            text = f.read()
        with open(anonymized_file, mode='r') as f:
            text_anonymized = f.read()
        anonymized_document_name = file_name[0:len(
            file_name)-4] + '_anonymized.odt'

    elif file_type == 'txt':
        text = Document.objects.filter(id=1)
        file_name = filename
        l = len(file_name)
        anonymized_file_name = file_name[0:(
            l-4)] + '_anonymized' + file_name[(l-4):l]

        command = ('python3 -m anonymizer_service -i ' + file +
                   ' -o upload_file/documents/' + user_folder + anonymized_file_name + " -w '" + custom_words + "'")
        runShell(command)

        anonymized_file = os.path.join(os.path.dirname(__file__),
                                       'documents/' + user_folder + anonymized_file_name)

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
