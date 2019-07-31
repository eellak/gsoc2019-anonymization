from django.http import HttpResponse, Http404
import requests
from pages.external_functions import create_user_folders
from upload_file.external_functions import anonymize_file, clear_user_dictionary
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
import subprocess
from os import system as runShell
from django.conf import settings
from .models import Document, User
from django.shortcuts import render, redirect
from .forms import UploadDocumentForm
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
import os


# from .forms import ModelFormWithFileField
# from .models import ModelWithFileField

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

user_folder = 'usr1'
files_folder = 'files'


def file_download(url, path, chunk=2048):
    req = requests.get(url, stream=True)
    if req.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in req.iter_content(chunk):
                f.write(chunk)
            f.close()
        return path
    raise Exception(
        'Given url is return status code:{}'.format(req.status_code))


def handle_uploaded_file(f, name='temp.txt', user_folder='default', user='anonymous'):
    script_dir = os.path.dirname(__file__)
    rel_path = "documents/" + user_folder + '/' + files_folder + '/' + name
    abs_file_path = os.path.join(script_dir, rel_path)

    l = len(abs_file_path)
    anonymized_rel_path = ("documents/" + user_folder + '/' +
                           name[0:len(name)-4] + '_anonymized' + name[len(name)-4: len(name)])
    anonymized_file_path = os.path.join(script_dir, anonymized_rel_path)
    # Write file
    with open(abs_file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    with open(abs_file_path, 'r', errors='ignore') as destination:
        text = destination.read()
        # text = unicode(text, errors='ignore')

    # Save file to database
    Document.objects.create(name=name, text=text,
                            file=abs_file_path, user_text=user, path=abs_file_path, anonymized_file_path=anonymized_file_path)


def upload_file(request):
    user_name = request.user
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            keepfiles = []
            user_obj = User.objects.filter(name=user_name)
            for cnt, afile in enumerate(files):
                handle_uploaded_file(
                    afile,
                    name=afile.name,
                    user_folder=str(request.user),
                    user=str(request.user)
                )
                filename_for_session = 'file' + str(cnt)
                request.session[filename_for_session] = afile.name

                keepfiles.append(afile.name)
                request.session['filenames'] = keepfiles
            return HttpResponseRedirect('/document/list/')
        else:
            print('not valid form')
    else:
        # GET METHOD

        create_user_folders(request=request)
        form = UploadDocumentForm()
        # If user exists do nothing
        user_obj = User.objects.filter(name=user_name)
        # print('user obj', user_obj)
        # print(f'hope to be none User{User.objects.none()}')
        if not user_obj:  # == User.objects.none():
            # print('user does not exist')
            user_obj = User(name=request.user, user_dictionary='')
            user_obj.save()
        else:
            user_obj = user_obj[0]
            # print(f'user {user_obj.name} exists')
            pass
    return render(request, 'home.html', {'form': form})


def document_list(request):

    # Get all documents from database
    queryset = Document.objects.filter(user_text=str(request.user))
    # queryset = Document.objects.order_by().values_list('name', flat=True).distinct()
    user_folder = (str(request.user))
    script_dir = os.path.dirname(__file__)
    rel_path = "documents/" + user_folder + '/' + files_folder
    abs_file_path = os.path.join(script_dir, rel_path)

    files = os.listdir(abs_file_path)

    # Get user words
    user_obj = User.objects.filter(name=str(request.user))
    if not user_obj:
        user_obj = User(name=request.user, user_dictionary='')
    else:
        user_obj = user_obj[0]
    words = user_obj.user_dictionary
    user_words = []
    new_dict = ''
    for word in words.split(','):
        if word in ['', "'", '"', "", " ", "", None]:
            continue
        # print(word)
        if word not in user_words:
            user_words.append(word)
            new_dict += word + ','
    user_obj.user_dictionary = new_dict
    user_obj.save()

    context = {
        'filenames': files,
        'files_path': os.path.join(script_dir, "documents/" + user_folder),
        'object_list': queryset,
        'user_dictionary': user_words
    }

    return render(request, 'document_list.html', context)


def document_delete(request, id):
    query = Document.objects.filter(id=id).delete()
    return HttpResponseRedirect('/document/list/')


def delete_user_dictionary(request, word):
    word = word.strip().replace('"', '')
    user_obj = User.objects.get(name=str(request.user))
    new_dict = user_obj.user_dictionary.replace(word + ',', '')
    new_dict = new_dict.replace(word, '')
    user_obj.user_dictionary = new_dict
    user_obj.save()
    return redirect('/document/list/')


def document_download(request, id):

    doc_obj = Document.objects.get(id=id)
    # print(doc_obj.anonymized_file_path)
    file_path = doc_obj.anonymized_file_path
    # print(f'anonymized_file{file_path}')

    if not os.path.exists(file_path):
        # File was not previewed so create it first
        [document,
         document_anonymized] = anonymize_file(id=id,
                                               user_folder=doc_obj.user_text,
                                               files_folder='files',
                                               custom_words='',
                                               text='',
                                               download=True)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(
            fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + \
            os.path.basename(file_path)
    return response
    # return redirect('/document/list/')
    # raise Http404


def document_preview(request, id):

    if request.method == 'GET':

        # Get user details
        user_name = request.user
        user_obj = User.objects.filter(name=user_name)
        # print(user_obj)
        if not user_obj:
            # print('user does not exist')
            user_obj = User(name=request.user, user_dictionary='')
            user_obj.save()
        else:
            # print('user {user_obj[0].name} exists')
            pass

        # Get user instance
        user_obj = User.objects.get(name=user_name)
        # Get object instance
        doc_obj = Document.objects.get(id=id)

        text = doc_obj.text
        anonymized_words = doc_obj.anonymized_words
        updateTextParameter = False

        # GET method text_parameters
        url = request.get_full_path()
        words = request.GET.getlist('text_param')
        custom_words = ''

        # GET method user_parameters
        url = request.get_full_path()
        user_words = request.GET.getlist('user_dictionary_param')
        user_custom_words = ''

        if words != []:
            # Make sure that we anonymize these words too.
            custom_words = words[0]
            l = len(custom_words)
            custom_words = custom_words[1:l-1]
            custom_words = custom_words.replace("\\n", "")
            # print('custom words:', custom_words)
            anonymized_words += custom_words
            anonymized_words += ','
            # print('anonymized_words', anonymized_words)
            # Update anonymized words by user in database
            Document.objects.filter(id=id).update(
                anonymized_words=anonymized_words)
            updateTextParameter = True

        user_anonymized_words = ''
        if user_words != []:
            # Make sure that we anonymize these words too.
            user_custom_words = user_words[0]
            l = len(user_custom_words)
            user_custom_words = user_custom_words[1:l-1]
            user_custom_words = user_custom_words.replace("\\n", "")
            user_anonymized_words += user_custom_words
            user_anonymized_words += ','
            # Update anonymized words by user in database
            user_obj = User.objects.get(name=user_name)
            user_obj.user_dictionary += user_anonymized_words
            user_obj.save()

        # Get user anonymized words from db
        user_anonymized_words = User.objects.filter(
            name=str(request.user))[0].user_dictionary + (user_anonymized_words if user_words != [] else '')
        # print(user_anonymized_words)
        user_folder = str(request.user)

        clear_user_dictionary(user_name=user_obj.name)

        # Check for possible updates
        # If the user dictionary version is not up to date
        # make sure to update it and re-render the text
        if doc_obj.copy_of_user_dictionary != user_obj.user_dictionary:
            # Update the copy user dictionary
            print(doc_obj.copy_of_user_dictionary, user_obj.user_dictionary)
            doc_obj.copy_of_user_dictionary = user_obj.user_dictionary
            doc_obj.save()
            # Make sure that the text is re rendered
            rerender_text = True
        else:
            rerender_text = False
        print(f'updateTextParameter={updateTextParameter}')
        print(f'rerender_text={rerender_text}')
        [document, document_anonymized] = anonymize_file(
            id=id,
            user_folder=user_folder,
            files_folder=files_folder,
            custom_words=(anonymized_words + ',' + user_anonymized_words),
            text=text,
            updateTextIfPossible=updateTextParameter,
            rerender_text=rerender_text)

        context = {
            'document': document,
            'document_anonymized': document_anonymized

        }
        # Clear variables
        anonymized_words = ''
        custom_words = ''
        words = []
        return render(request, 'document_preview.html', context)


def delete_anonymized_words(request, id):
    Document.objects.filter(id=id).update(anonymized_words='')
    new_url = '/document/preview/' + str(id) + '?text_param=[""]'
    return redirect(new_url)


# content = ContentFile(base64.b64decode(fileData))
# speaker.profile_file.save(filename, content)
# speaker.save()
