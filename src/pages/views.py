from django.shortcuts import render
from upload_file.views import upload_file

# Create your views here.


def home_view(request, *args, **kwargs):
    # file_uploader = upload_file(request=request)
    return render(request, "home.html", {})


def about_view(request, *args, **kwargs):
    return render(request, 'about.html', {})


def contact_view(request, *args, **kwargs):
    return render(request, 'contact.html', {})
