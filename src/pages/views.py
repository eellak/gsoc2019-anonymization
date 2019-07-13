from django.shortcuts import render
from upload_file.views import upload_file
from os import system as runShell
import os
# Create your views here.


def clear_documents_on_redirect():
    path = os.path.dirname(__file__)
    rel_path = '../upload_file/documents/'
    abs_path = os.path.join(path, rel_path)
    command = 'cd ' + abs_path + ';rm *;'

    runShell(command=command)


def home_view(request, *args, **kwargs):
    # file_uploader = upload_file(request=request)
    clear_documents_on_redirect()
    return render(request, "home.html", {})


def about_view(request, *args, **kwargs):
    clear_documents_on_redirect()
    return render(request, 'about.html', {})


def contact_view(request, *args, **kwargs):
    clear_documents_on_redirect()
    return render(request, 'contact.html', {})
