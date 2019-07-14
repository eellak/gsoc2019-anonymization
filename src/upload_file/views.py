import os
from django.http import HttpResponseRedirect
from .forms import UploadDocumentForm
from django.shortcuts import render
from .models import Document
from django.conf import settings
from os import system as runShell
import subprocess
from django.views.generic.edit import FormView
from django.contrib.auth.models import User


# from .forms import ModelFormWithFileField
# from .models import ModelWithFileField

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

user_folder = 'usr1/'
files_folder = 'files/'


def handle_uploaded_file(f, name='temp.txt'):
    script_dir = os.path.dirname(__file__)
    rel_path = "documents/" + user_folder + files_folder + name
    # + str(User)
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            keepfiles = []
            for cnt, afile in enumerate(files):
                handle_uploaded_file(
                    afile, name=afile.name)
                filename_for_session = 'file' + str(cnt)
                request.session[filename_for_session] = afile.name

                keepfiles.append(afile.name)
                request.session['filenames'] = keepfiles
            return HttpResponseRedirect('/document/list')
        else:
            print('not valid form')
    else:
        form = UploadDocumentForm()
    return render(request, 'home.html', {'form': form})


def document_list(request):

    script_dir = os.path.dirname(__file__)
    rel_path = "documents/" + user_folder + files_folder
    abs_file_path = os.path.join(script_dir, rel_path)

    files = os.listdir(abs_file_path)

    context = {
        'filenames': files
    }

    return render(request, 'document_list.html', context)


def document_preview(request):

    text = ''
    file = os.path.join(os.path.dirname(__file__),
                        'documents/' + user_folder + files_folder + request.session['file'])
    directory = os.path.dirname(__file__)
    command = 'cd ' + directory
    runShell(command)
    command = 'cd ..'
    runShell(command)
    file_type = request.session['file'][-3:]

    if file_type == 'odt':

        file_name = request.session['file']
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
                   tempname)
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
        command = ('python3 -m anonymizer_service -i upload_file/documents/' + user_folder + files_folder +
                   request.session['file'])
        runShell(command)

        file_name = request.session['file']
        l = len(file_name)
        anonymized_file_name = file_name[0:(
            l-4)] + '_anonymized' + file_name[(l-4):l]
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

    document = {
        'name': request.session['file'],
        'text': text,
        'type': file_type,
        'error': file_error
    }

    document_anonymized = {
        'name': anonymized_document_name,
        'text': text_anonymized,
        'type': file_type,
        'error': file_error
    }

    context = {
        'document': document,
        'document_anonymized': document_anonymized

    }
    return render(request, 'document_preview.html', context)
