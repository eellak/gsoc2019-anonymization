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

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default='')
    file = models.FileField()
    documents = models.ForeignKey(
        UserDocuments, on_delete=models.CASCADE, default=None, null=True)
    path = models.TextField(default='')
    anonymized_file_path = models.TextField(default='')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True)
    user_text = models.CharField(max_length=200, default='anonymous')
    text = models.TextField(default='')
    anonymized_words = models.TextField(default='')
    copy_of_user_dictionary = models.TextField(default='')
    delete_words = models.TextField(default='')

    def __str__(self):
        return str(self.name)

    # def get_absolute_url(self):
    #     return reverse("document-list", kwargs={"pk": self.pk})


class User(models.Model):
    name = models.CharField(
        primary_key=True, max_length=200, default='anonymous')
    user_dictionary = models.TextField(default='')

    def __str__(self):
        return str(self.name)
