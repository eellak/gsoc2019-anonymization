from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render
from .models import Document
# from .forms import ModelFormWithFileField
# from .models import ModelWithFileField

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

# Create your views here.


def upload_file_container_view(request):
    context = {}
    return render(request, 'upload_file/upload_file_container.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            print('valid form')
            # handle_uploaded_file(request.FILES['file'])
            uploaded_file = request.FILES['file']
            print(uploaded_file.name)
            print(uploaded_file.size)
            # print('akolouthoun doc kai title')
            # print(form.cleaned_data['document'])
            # print(form.cleaned_data['title'])
            # print(form.cleaned_data['x'])

            return HttpResponseRedirect('/home/')
        else:
            print('not valid form')
    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})
