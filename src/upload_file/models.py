from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from .forms import UploadDocumentForm
# from .models import ModelWithFileField

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserDocuments(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    # text = models.TextField(blank=False, max_length=500)


class Document(models.Model):
    # title = models.CharField(max_length=200, default='')
    file = models.FileField()
    documents = models.ForeignKey(
        UserDocuments, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    slug = models.SlugField(max_length=40, default=file.name)
