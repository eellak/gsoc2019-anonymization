from os import system as runShell
import os


def clear_documents_on_redirect(request):
    path = os.path.dirname(__file__)
    rel_path = '../upload_file/documents/'
    abs_path = os.path.join(path, rel_path)
    command = 'cd ' + abs_path + ';rm -r *;'

    runShell(command=command)


def create_user_folders(request, *args, **kwargs):
    user = str(request.user)
    user_dir = user + '/'
    path = os.path.dirname(__file__)
    rel_path = '../upload_file/documents/'
    abs_path = os.path.join(path, rel_path)
    if not os.path.exists(abs_path + user_dir):
        os.makedirs(abs_path + user_dir)
        if not os.path.exists(abs_path + user_dir + 'files/'):
            os.makedirs(abs_path + user_dir + 'files/')
