from django import forms

from .models import Document, UserDocuments
from django.forms import ClearableFileInput


class UploadDocumentForm(forms.ModelForm):
    # path = forms.CharField(required=False)

    class Meta:
        model = Document
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }


class UploadMultipleDocumentsForm(forms.ModelForm):
    class Meta:
        model = UserDocuments
        fields = []
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }
