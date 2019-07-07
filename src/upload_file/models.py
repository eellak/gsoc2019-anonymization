from django.db import models

# Create your models here.
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from .forms import UploadFileForm
# from .models import ModelWithFileField


class Document(models.Model):
    # title = models.CharField(max_length=200, default='')
    file = models.FileField()
