from os import system
import os
from unotools.component.writer import Writer
from unotools.unohelper import convert_path_to_url
from unotools import Socket, connect
import uno
from com.sun.star.beans import PropertyValue
from shutil import copy2
import subprocess
import json


# Some global variables
files_folder = '/tmp/libreoffice/anonymizer_extension/extension_files/'
tempfile = files_folder + 'tempfile.odt'
tempanonymizedfile = (files_folder + 'tempfile_anonymized.odt')
words_file = files_folder + '/words.txt'
settings_file = files_folder + '/settings.json'


def init():
    # system("soffice --accept='socket,host=localhost,port=8100;urp;StarOffice.Service'")

    context = connect(Socket('localhost', 8100))
    writer = Writer(context)

    custom_text = 'this is the custom text'
    writer.set_string_to_end(custom_text)
    text = writer.text
    print('this is the text:', text.getString())

    filename = './myfile.odt'
    url = convert_path_to_url(filename)
    writer.store_to_url(url, 'FilterName', 'writer8')
    writer.close(True)


def list_of_added_words():
    result = subprocess.run(['which', 'gedit'], stdout=subprocess.PIPE)
    if str(result.stdout) != "b''":
        if file_exists(words_file):
            # Remove \n and b''
            # Open the word file
            gedit_exec = str(result.stdout)
            l = len(gedit_exec)
            gedit_exec = gedit_exec[2:len(gedit_exec)-3]
            command = (gedit_exec + ' ' + words_file)
            system(command=command)
        else:
            # File doesn't exist so do nothing
            pass


def get_document_name(ifile):
    xModel = XSCRIPTCONTEXT.getDocument()
    url = xModel.getLocation().replace('file://', '')
    return url


def file_exists(ifile=None):
    if os.path.isfile(ifile):
        # This means that file exists
        return True
    return False


def get_selected_words():
    import os
    # Check if file exists else []
    if not os.path.isfile(words_file):
        return []
    # File exists
    with open(words_file, mode='r') as f:
        text = f.read().replace('<selected_word>', '').replace(
            '<end_of_selected_word>', '')
        print(f'text={text}')
        words = text.split(',')
        print(f'words={words}')
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
            word_to_be_written = (
                '<selected_word>' +
                word +
                '<end_of_selected_word>' +
                ','
            )
            f.write(word_to_be_written)


def my_first_macro_writer():
    doc = XSCRIPTCONTEXT.getDocument()
    text = doc.getText()
    text.setString('Hello World in Python in Writer')
    return


def getNewString(theString):
    if(not theString or len(theString) == 0):
        return ""
    # should we tokenize on "."?
    if theString[0].isupper() and len(theString) >= 2 and theString[1].isupper():
        # first two chars are UC => first UC, rest LC
        newString = theString[0:1].upper() + theString[1:].lower()
    elif theString[0].isupper():
        # first char UC => all to LC
        newString = theString.lower()
    else:  # all to UC.
        newString = theString.upper()
    return newString


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
        print(ifile, 'ifile was given')
        print(ofile, 'ofile was given')
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
            xText = xTextRange.getText()
            xWordCursor = xText.createTextCursorByRange(xTextRange)
            if not xWordCursor.isStartOfWord():
                xWordCursor.gotoStartOfWord(False)
            xWordCursor.gotoNextWord(True)
            theString = xWordCursor.getString()
            newString = getNewString(theString)
            if newString:
                xWordCursor.setString(newString)
                xSelectionSupplier.select(xWordCursor)
        else:

            newString = getNewString(theString)
            if newString:
                xTextRange.setString(newString)
                xSelectionSupplier.select(xTextRange)
                word += newString
                print(f'newString added: {newString}')
        i += 1
        # if (theString in [' ', '\n', '\r']):
        #     pass
    print(f'word={word}')
    selected_words.append(word)
    print(f'selected_words = {selected_words}')
    set_selected_words(selected_words)
    anonymize_document(with_words=True)
    reload_document()


def anonymize_document(with_words=False):

    import string
    import os

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
    # print(url)
    copy2(src=url, dst=tempfile)
    # curr_args = xModel.getArgs()
    # xModel.storeAsURL(tempfile, curr_args)
    # xModel.storeToURL(tempfile, curr_args)

    # the writer controller impl supports the css.view.XSelectionSupplier interface
    xSelectionSupplier = xModel.getCurrentController()

    # Try to get the text
    xAllText = xModel.Text

    textString = xAllText.getString()

    xAllTextAnonymized = call_anonymizer_service(
        text=None,
        words=get_selected_words(),
        ifile=tempfile,
        ofile=tempanonymizedfile
    )

    # Copy file to the new location
    if not file_exists(ifile=words_file) or with_words == False:
        new_dest = url[0:len(url)-4] + '_anonymized.odt'
    else:
        # new_dest = new_dest, remains as it is
        # Now we need a temp file
        # Remove the already opened file.
        # command = 'rm ' + url + ' &'
        # system(command=command)
        # Now set the new location as the existing file
        # that we just deleted.
        # new_dest = (url[0:len(url)-4] + '_anonymized' +
                    # get_document_number(url)+'.odt')
        new_dest = url

    # Now copy the file
    copy2(src=tempanonymizedfile, dst=new_dest)
    command = ('libreoffice --writer --nofirststartwizard ' +
               new_dest + ' &')
    system(command=command)

    # xAllText.setString(xAllTextAnonymized)


# lists the scripts, that shall be visible inside OOo. Can be omitted, if
# all functions shall be visible, however here getNewString shall be suppressed
g_exportedScripts = (anonymize_document,
                     anonymize_selected_text,
                     list_of_added_words,
                     reload_document
                     )


if __name__ == "__main__":
    init()
