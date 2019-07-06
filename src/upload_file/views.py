from django.shortcuts import render

# Create your views here.


def upload_file_container_view(request):
    context = {}
    return render(request, 'upload_file/upload_file_container.html', context)
