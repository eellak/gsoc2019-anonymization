import requests
from pages.external_functions import create_user_folders
from upload_file.external_functions import anonymize_file
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
import subprocess
from os import system as runShell
from django.conf import settings
from .models import Document
from django.shortcuts import render, redirect
from .forms import UploadDocumentForm
from django.http import HttpResponseRedirect
import os


# from .forms import ModelFormWithFileField
# from .models import ModelWithFileField

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

custom_words = ''
user_folder = 'usr1/'
files_folder = 'files/'


def file_download(url, path, chunk=2048):
    req = requests.get(url, stream=True)
    if req.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in req.iter_content(chunk):
                f.write(chunk)
            f.close()
        return path
    raise Exception(
        'Given url is return status code:{}'.format(req.status_code))


def handle_uploaded_file(f, name='temp.txt', user_folder='usr1/', user='anonymous'):
    script_dir = os.path.dirname(__file__)
    rel_path = "documents/" + user_folder + files_folder + name
    # + str(User)
    abs_file_path = os.path.join(script_dir, rel_path)
    # text = ''

    with open(abs_file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    with open(abs_file_path, 'r', errors='ignore') as destination:
        text = destination.read()
        # text = unicode(text, errors='ignore')

    Document.objects.create(name=name, text=text,
                            file=abs_file_path, user_text=user)

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
                    user_folder=str(request.user) + '/',
                    user=str(request.user)
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

    # Get all documents from database
    queryset = Document.objects.filter(user_text=str(request.user))
    # queryset = Document.objects.order_by().values_list('name', flat=True).distinct()
    user_folder = (str(request.user) + '/')
    script_dir = os.path.dirname(__file__)
    rel_path = "documents/" + user_folder + files_folder
    abs_file_path = os.path.join(script_dir, rel_path)

    files = os.listdir(abs_file_path)

    context = {
        'filenames': files,
        'files_path': os.path.join(script_dir, "documents/" + user_folder),
        'object_list': queryset
    }

    return render(request, 'document_list.html', context)


def document_delete(request, id):
    query = Document.objects.filter(id=id).delete()
    return HttpResponseRedirect('/document/list/')


def document_download(request, id):
    query = Document.objects.filter(id=id).filter(user_text=str(request.user))

    # file_download(url='hello', path=)


def document_preview(request, id):
    url = request.get_full_path()
    words = request.GET.getlist('param')
    custom_words = ''
    if words != []:
        # Make sure that we anonymize these words too.
        custom_words = words[0]
        # print(*words)
        # print(custom_words)
        l = len(custom_words)
        custom_words = custom_words[1:l-1]
        custom_words = custom_words.replace("\\n", "")
        print('custom words:', custom_words)
    user_folder = str(request.user) + '/'
    [document, document_anonymized] = anonymize_file(
        id=id,
        user_folder=user_folder,
        files_folder=files_folder,
        custom_words=custom_words)

    context = {
        'document': document,
        'document_anonymized': document_anonymized

    }
    return render(request, 'document_preview.html', context)
