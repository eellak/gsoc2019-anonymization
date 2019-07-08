from django.contrib import admin
from django.urls import path
from .views import document_preview

# document app
app_name = 'documents'
urlpatterns = [
    path('preview/', document_preview, name='document-preview')
]
