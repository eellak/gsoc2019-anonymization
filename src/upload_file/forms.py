from django import forms


class UploadFileForm(forms.Form):
    # path = forms.CharField(required=False)
    document = forms.FileField()
    title = forms.CharField(
        max_length=50, required=False, initial='uploaded_file')
