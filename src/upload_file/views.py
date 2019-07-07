from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.shortcuts import render
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
        if form.is_valid():
            # handle_uploaded_file(request.FILES['file'])
            uploaded_file = request.FILES['document']
            print(uploaded_file.name)
            print(uploaded_file.size)

            return HttpResponseRedirect('/home/')
        else:
            print('not valid form')
    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})
