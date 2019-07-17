from django.contrib import admin
from django.urls import path, re_path
from .views import document_preview, document_list, document_delete

# document app
app_name = 'documents'
urlpatterns = [
    re_path(r'preview/(?P<filename>[\w\-.0-9]+)',
            document_preview, name='document-preview'),
    re_path(r'delete/(?P<id>[\w\-.0-9]+)',
            document_delete, name='document-delete'),

    path('list/', document_list, name='document-list')
]
