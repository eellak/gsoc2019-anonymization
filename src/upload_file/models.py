from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from .forms import UploadDocumentForm
# from .models import ModelWithFileField


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
        User, on_delete=models.CASCADE)

    # def get_absolute_url(self):
    #     return reverse("documents:document-detail", kwargs={"pk": self.pk})
