from os import system
import uno
import os
from com.sun.star.beans import PropertyValue
from shutil import copy2
import subprocess
import json


# Some global variables
specific_file_folder = ''
files_folder = ('/tmp/libreoffice/anonymizer_extension/extension_files/' +
                specific_file_folder)
tempfile = files_folder + 'tempfile.odt'
tempanonymizedfile = (files_folder + 'tempfile_anonymized.odt')
words_file = files_folder + '/words.txt'
settings_file = files_folder + '/settings.json'
helptext_file = files_folder + '/helptext.txt'

helptext = '''
This python script contains the following libreoffice macros:

 - init: This macro should always be runned first, in order to set up
         all important files for the service.

 - anonymize_document: This macro should always be runned after init.
                       It anonymizes the whole document and opens a new file
                       for further anonymization. This function uses the basic
                       patterns of anonymizer.

 - anonymize_selected_text: This macro anonymizes the selected text.
                            Caution: This macro should NEVER be runned before init or
                            anonymize_document.Otherwise it will replace the original
                            document saving the new one over the original.

 - list_of_added_words: This macro previews all the words that user has selected
                        for anonymization. User can always delete any word that he had
                        previously selected. If user changes and saves the file, then in order
                        to see the changes, user has to run the following script.
                        If user wants to delete a word, for example Δημήτρης he has
                        to delete the whole line:
                        <selected_word>Δημήτρης<end_of_selected_word>,

 - reload_changes : This macro reloads the document after user removes any word.

 Author: Dimitris Katsiros
 Implemented for GFOSS during GSoC 2019.
 Original repository: https://www.github.com/eellak/gsoc2019-anonymization
'''


def update_folder_paths():
    global files_folder, tempfile, tempanonymizedfile, words_file, settings_file, helptext_file
    files_folder = ('/tmp/libreoffice/anonymizer_extension/extension_files/' +
                    specific_file_folder)
    tempfile = files_folder + 'tempfile.odt'
    tempanonymizedfile = (files_folder + 'tempfile_anonymized.odt')
    words_file = files_folder + '/words.txt'
    settings_file = files_folder + '/settings.json'
    helptext_file = files_folder + '/helptext.txt'


def init():

    import string

    original_file = get_document_name()
    # Create the specific folder
    global specific_file_folder
    specific_file_folder = get_specific_file_folder(ifile=original_file)
    # Update all folders paths dynamically
    update_folder_paths()

    # Check some things first
    # Folders etc.
    if not os.path.isdir(files_folder):
        # Create the folder
        access_rights = 0o755
        os.makedirs(files_folder, access_rights)

    # Save settings
    data = {
        'original_file': original_file,
        'specific_file_folder': specific_file_folder,
        'files_folder': files_folder

    }

    with open(settings_file, mode='w+') as settings:
        json.dump(data, settings)


def helpme():

    if not os.path.exists(settings_file):
        # User has not yet runned init but wants help
        init()
    with open(helptext_file, mode='w+') as f:
        # Always rewrite the help file. User may delete or change
        # the original file at any time. Overwrite it.
        f.write(helptext)
    # Preview the file for help
    preview_file(editor='gedit', ifile=helptext_file)


def get_from_settings(request):
    with open(settings_file, mode='r') as settings:
        data = json.load(settings)
        return data[request]


def reload_changes():
    original_file = get_from_settings('original_file')
    reload = {
        'original_file': original_file
    }
    anonymize_document(with_words=True, reload=reload)
    reload_document()


def preview_file(editor='gedit', ifile=helptext_file):
    result = subprocess.run(['which', editor], stdout=subprocess.PIPE)
    if str(result.stdout) != "b''":
        if file_exists(ifile):
            # Remove \n and b''
            # Open the word file
            gedit_exec = str(result.stdout)
            l = len(gedit_exec)
            gedit_exec = gedit_exec[2:len(gedit_exec)-3]
            command = (gedit_exec + ' ' + ifile + ' &')
            system(command=command)
        else:
            result = subprocess.run(['which', 'vim'], stdout=subprocess.PIPE)
            if str(result.stdout) != "b''":
                if file_exists(ifile):
                    # Remove \n and b''
                    # Open the word file
                    vim_exec = str(result.stdout)
                    l = len(vim_exec)
                    vim_exec = vim_exec[2:len(vim_exec)-3]
                    command = (vim_exec + ' ' + ifile + ' &')
                    system(command=command)
            else:
                command = ('vi' + ' ' + ifile + ' &')
                system(command=command)


def get_specific_file_folder(ifile=None):
    if ifile == None:
        return ''
    # Return the name of file without extension
    ifile = ifile.split('/')
    name = ifile[len(ifile)-1]
    return name[0:len(name)-4].replace('.', '') + '/'


def list_of_added_words():
    # Otherwise known as list of selected words.
    # Each word in the file has the following form:
    #   <selected_word>here is \nthe word\n<end_of_selected_word>,
    # By calling this function all the selected words are previewed
    # to the user.
    preview_file(editor='gedit', ifile=words_file)


def get_document_name():
    xModel = XSCRIPTCONTEXT.getDocument()
    url = xModel.getLocation().replace('file://', '')
    return url


def file_exists(ifile=None):
    if os.path.isfile(ifile):
        # This means that file exists
        return True
    return False


def get_selected_words():

    # Check if file exists else []
    if not os.path.isfile(words_file):
        return []
    # File exists
    with open(words_file, mode='r') as f:
        text = f.read().replace('\n<selected_word>', '').replace(
            '<end_of_selected_word>', '')
        words = text.split(',')
        # return words

    # Clear words
    cleared_words = []
    for word in words:
        if word != '':
            cleared_words.append(word)
    return cleared_words


def set_selected_words(words=[]):
    with open(words_file, mode='a') as f:
        for word in words:
            if word in ['', ' ', None]:
                continue
            word_to_be_written = (
                '\n<selected_word>' +
                word +
                '<end_of_selected_word>' +
                ','
            )
            f.write(word_to_be_written)


def call_anonymizer_service(text=None, words=[], ifile=None, ofile=None):
    # from os import system
    from anonymizer.anonymize import find_entities
    if text != None:
        # Write text to a temp file
        with open(tempfile, mode='w') as open_file:
            open_file.write(text)
        find_entities(ifile=tempfile,
                      ofile=ofile,
                      method=['strict', "*", "True"],
                      patterns_file='patterns.json',
                      verbose=False,
                      words_array=words,
                      libreoffice=True)
    # If ifile is given
    else:
        find_entities(ifile=ifile,
                      ofile=ofile,
                      method=['strict', "*", "True"],
                      patterns_file='patterns.json',
                      verbose=False,
                      words_array=words)

    # # Read the output file

    # with open(ofile, mode='r') as ofile:
    #     text = ofile.read()

    # # Now return the anonymized text to be written
    # return text


def reload_document():

    from pynput.keyboard import Key, Controller
    import time
    keyboard = Controller()
    keyboard.press(Key.shift)
    time.sleep(0.05)
    keyboard.press(Key.f7)
    keyboard.release(Key.shift)
    keyboard.release(Key.f7)


def anonymize_selected_text():
    """Change the case of a selection, or current word from upper case, to first char upper case, to all lower case to upper case..."""
    import string
    selected_words = []
    word = ''
    # The context variable is of type XScriptContext and is available to
    # all BeanShell scripts executed by the Script Framework
    xModel = XSCRIPTCONTEXT.getDocument()

    # the writer controller impl supports the css.view.XSelectionSupplier interface
    xSelectionSupplier = xModel.getCurrentController()

    # see section 7.5.1 of developers' guide
    xIndexAccess = xSelectionSupplier.getSelection()
    count = xIndexAccess.getCount()
    if(count >= 1):  # ie we have a selection
        i = 0
    while i < count:
        xTextRange = xIndexAccess.getByIndex(i)
        # print "string: " + xTextRange.getString();
        theString = xTextRange.getString()
        if len(theString) == 0:
            # sadly we can have a selection where nothing is selected
            # in this case we get the XWordCursor and make a selection!
            # xText = xTextRange.getText()
            # xWordCursor = xText.createTextCursorByRange(xTextRange)
            # if not xWordCursor.isStartOfWord():
            #     xWordCursor.gotoStartOfWord(False)
            # xWordCursor.gotoNextWord(True)
            # theString = xWordCursor.getString()
            # newString = getNewString(theString)
            # if newString:
            #     xWordCursor.setString(newString)
            #     xSelectionSupplier.select(xWordCursor)
            pass
        else:

            newString = theString  # getNewString(theString)
            if newString:
                xTextRange.setString(newString)
                xSelectionSupplier.select(xTextRange)
                word += newString
        i += 1
    if word in [' ', '\n', '\r', '']:
        return
    selected_words.append(word)
    set_selected_words(selected_words)
    anonymize_document(with_words=True)
    reload_document()


def anonymize_document(with_words=False, reload={}):

    import string

    # Check some things first
    # Folders etc.

    if not os.path.isdir(files_folder):
        # Create the folder
        access_rights = 0o755
        os.makedirs(files_folder, access_rights)

    # The context variable is of type XScriptContext and is available to
    # all BeanShell scripts executed by the Script Framework
    xModel = XSCRIPTCONTEXT.getDocument()
    # Save the document
    xModel.store()
    url = xModel.getLocation().replace('file://', '')
    copy2(src=url, dst=tempfile)
    # curr_args = xModel.getArgs()
    # xModel.storeAsURL(tempfile, curr_args)
    # xModel.storeToURL(tempfile, curr_args)

    # the writer controller impl supports the css.view.XSelectionSupplier interface
    xSelectionSupplier = xModel.getCurrentController()

    # Try to get the text
    xAllText = xModel.Text

    textString = xAllText.getString()

    if reload != {}:
        # This means you should reload the file
        original_file = reload['original_file']
        xAllTextAnonymized = call_anonymizer_service(
            text=None,
            words=get_selected_words(),
            ifile=original_file,
            ofile=tempanonymizedfile
        )
    else:
        # This is the usual case
        xAllTextAnonymized = call_anonymizer_service(
            text=None,
            words=get_selected_words(),
            ifile=tempfile,
            ofile=tempanonymizedfile
        )

    # if get_selected_words() != []:
    #     with_words = True
    # Copy file to the new location
    if not file_exists(ifile=words_file) or with_words == False:
        new_dest = url[0:len(url)-4] + '_anonymized.odt'
        # Now copy the file
        copy2(src=tempanonymizedfile, dst=new_dest)
        command = ('libreoffice --writer --nofirststartwizard ' +
                   new_dest + ' &')
        system(command=command)
    else:
        new_dest = url
        # Now copy the file
        copy2(src=tempanonymizedfile, dst=new_dest)


# lists the scripts, that shall be visible inside OOo. Can be omitted, if
# all functions shall be visible, however here getNewString shall be suppressed
g_exportedScripts = (init,
                     anonymize_document,
                     anonymize_selected_text,
                     list_of_added_words,
                     reload_changes,
                     helpme
                     )


if __name__ == "__main__":
    helpme()
