from django.contrib import admin
from django.urls import path, re_path
from .views import document_preview, document_list

# document app
app_name = 'documents'
urlpatterns = [
    re_path(r'preview/(?P<filename>[\w\-.]+)',
            document_preview, name='document-preview'),
    path('list/', document_list, name='document-list')
]
