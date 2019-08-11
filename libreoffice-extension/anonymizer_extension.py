from os import system
from unotools.component.writer import Writer
from unotools.unohelper import convert_path_to_url
from unotools import Socket, connect

# Some global variables
files_folder = '/tmp/libreoffice/anonymizer_extension/extension_files/'
tempfile = files_folder + 'tempfile.odt'
tempanonymizedfile = (files_folder + 'tempfile_anonymized.odt')


def init():
    system("soffice --accept='socket,host=localhost,port=8100;urp;StarOffice.Service'")

    context = connect(Socket('localhost', 8100))
    writer = Writer(context)

    custom_text = 'this is the custom text'
    writer.set_string_to_end(custom_text)
    text = writer.text

    filename = './myfile.odt'
    url = convert_path_to_url(filename)
    writer.store_to_url(url, 'FilterName', 'writer8')
    writer.close(True)


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


def capitalisePython():
    """Change the case of a selection, or current word from upper case, to first char upper case, to all lower case to upper case..."""
    import string

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
        i += 1


def call_anonymizer_service(text):
    # from os import system
    from anonymizer.anonymize import find_entities

    # Write text to a temp file
    with open(tempfile, mode='w') as open_file:
        open_file.write(text)
    # command = ("python3 -m anonymizer" +
    #            " -i " + tempfile_name +
    #            " -o " + tempanonymizedfile_name)
    # system(command=command)

    find_entities(ifile=tempfile,
                  ofile=tempanonymizedfile,
                  method=['strict', "*", "True"],
                  patterns_file='patterns.json',
                  verbose=False,
                  words_array=[],
                  libreoffice=True)

    # Read the output file

    with open(tempanonymizedfile, mode='r') as ofile:
        text = ofile.read()

    # Now return the anonymized text to be written
    return text


def anonymize_document():

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

    # the writer controller impl supports the css.view.XSelectionSupplier interface
    xSelectionSupplier = xModel.getCurrentController()

    # Try to get the text
    xAllText = xModel.Text
    textString = xAllText.getString()
    # xAllTextAnonymized = call_anonymizer_service(
    #     'My name is dimitris katsiros 6984442548')
    xAllTextAnonymized = call_anonymizer_service(textString)

    xAllText.setString(xAllTextAnonymized)


# lists the scripts, that shall be visible inside OOo. Can be omitted, if
# all functions shall be visible, however here getNewString shall be suppressed
g_exportedScripts = anonymize_document,


if __name__ == "__main__":
    init()
