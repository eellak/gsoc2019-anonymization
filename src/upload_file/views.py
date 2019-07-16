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
from upload_file.external_functions import anonymize_file
from pages.external_functions import create_user_folders

# from .forms import ModelFormWithFileField
# from .models import ModelWithFileField

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

user_folder = 'usr1/'
files_folder = 'files/'


def handle_uploaded_file(f, name='temp.txt', user_folder='usr1/'):
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
                    afile,
                    name=afile.name,
                    user_folder=str(request.user) + '/'
                )
                filename_for_session = 'file' + str(cnt)
                request.session[filename_for_session] = afile.name

                keepfiles.append(afile.name)
                request.session['filenames'] = keepfiles
            return HttpResponseRedirect('/document/list/')
        else:
            print('not valid form')
    else:
        create_user_folders(request=request)
        form = UploadDocumentForm()
    return render(request, 'home.html', {'form': form})


def document_list(request):

    user_folder = (str(request.user) + '/')
    script_dir = os.path.dirname(__file__)
    rel_path = "documents/" + user_folder + files_folder
    abs_file_path = os.path.join(script_dir, rel_path)

    files = os.listdir(abs_file_path)

    context = {
        'filenames': files
    }

    return render(request, 'document_list.html', context)


def document_preview(request, filename):

    user_folder = str(request.user) + '/'
    [document, document_anonymized] = anonymize_file(
        filename,
        user_folder=user_folder,
        files_folder=files_folder)

    context = {
        'document': document,
        'document_anonymized': document_anonymized

    }
    return render(request, 'document_preview.html', context)
