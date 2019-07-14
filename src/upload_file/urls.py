from django.contrib import admin
from django.urls import path
from .views import document_preview, document_list

# document app
app_name = 'documents'
urlpatterns = [
    path('preview/', document_preview, name='document-preview'),
    path('list/', document_list, name='document-list')
]
