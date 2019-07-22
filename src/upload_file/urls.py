from django.contrib import admin
from django.urls import path, re_path
from .views import document_preview, document_list, document_delete, document_download
# from filetransfers.api import serve_file

# document app
app_name = 'documents'
urlpatterns = [
    re_path(r'preview/(?P<id>[0-9]+)',
            document_preview, name='document-preview'),
    re_path(r'delete/(?P<id>[\w\-.0-9]+)',
            document_delete, name='document-delete'),
    re_path(r'download/(?P<id>[\w\-.0-9]+)',
            document_download, name='document-download'),
    path('list/', document_list, name='document-list')
]
