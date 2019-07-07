from django import forms

from .models import Document


class UploadFileForm(forms.ModelForm):
    # path = forms.CharField(required=False)

    class Meta:
        model = Document
        fields = [
            # 'title',
            'file'
        ]
