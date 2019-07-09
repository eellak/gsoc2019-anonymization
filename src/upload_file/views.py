import os
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render
from .models import Document
from django.conf import settings

# from .forms import ModelFormWithFileField
# from .models import ModelWithFileField

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file


def handle_uploaded_file(f, name='temp.txt'):
    script_dir = os.path.dirname(__file__)
    rel_path = "documents/" + name
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            print('valid form')
            uploaded_file = request.FILES['file']
            handle_uploaded_file(
                request.FILES['file'], name=uploaded_file.name)
            # request.session['file'] = request.FILES['file']
            print(uploaded_file.name)
            request.session['file'] = uploaded_file.name
            print(uploaded_file.size)
            return HttpResponseRedirect('/document/preview')
        else:
            print('not valid form')
    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})


def document_preview(request):
    print('document_previewed')

    text = ''
    file = os.path.join(os.path.dirname(__file__),
                        'documents/' + request.session['file'])

    with open(file, mode='r') as f:
        text = f.read()

    document = {
        'name': request.session['file'],
        'text': text
    }
    context = {
        'document': document,

    }
    return render(request, 'document_preview.html', context)
