from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from .views import document_preview, document_list, document_delete, document_download, delete_anonymized_words
# from filetransfers.api import serve_file

# document app
app_name = 'documents'
urlpatterns = [
    re_path(r'preview/(?P<id>[0-9]+)',
            document_preview, name='document-preview'),
    re_path(r'delete/(?P<id>[0-9]+)',
            document_delete, name='document-delete'),
    re_path(r'download/(?P<id>[0-9]+)',
            document_download, name='document-download'),
    re_path(r'delete_anonymized_words/(?P<id>[0-9]+)',
            delete_anonymized_words, name='document-delete-anonymized-words'),

    path('list/', document_list, name='document-list')
]
