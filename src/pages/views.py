from django.shortcuts import render
from upload_file.views import upload_file
from pages.external_functions import create_user_folders, clear_documents_on_redirect
# Create your views here.


def home_view(request, *args, **kwargs):
    # file_uploader = upload_file(request=request)
    # clear_documents_on_redirect(request)
    create_user_folders(request=request)
    return render(request, "home.html", {})


def about_view(request, *args, **kwargs):
    # clear_documents_on_redirect()
    return render(request, 'about.html', {})


def contact_view(request, *args, **kwargs):
    # clear_documents_on_redirect()
    return render(request, 'contact.html', {})
