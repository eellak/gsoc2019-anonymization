# Google Summer Of Code 2019 :sunny:

### Anonymisation Through Data Encryption of Sensitive Data in ODT and Text Files in Greek Language

## Problem Statement
Over the past year, great importance has been attached to information anonymisation from governments all around the world. The GDPR defines pseudonymization and the processing of personal data in such a way that the data can no longer be attributed to a specific data subject without the use of additional information. Although the GDPR has been implemented since 2018 no reliable infrastructure exists in Greece to encrypt sensitive documents. It is therefore necessary to develop a product specifically for users of the Greek language that can safely and promptly anonymize their data in order for it to abide to the GDPR.

## Abstract
I propose the creation of a LibreOffice extension as well as a web GUI that will anonymize information in any legal document given. All sensitive information should be easily anonymized through this open-source tool. 

On the subject of the creation of the anonymizer I suggest the following metrics. First of all, given any document the anonymizer should encrypt any greek entity in the file from a standard token vocabulary set. The user will be able to add specific arguments for entities to be anonymized (in addition to the standard ones) and he will be given the option to choose for an additional encryption. I believe that the LibreOffice extension as well as the web GUI should be user-friendly so customizable technologies should be used.


## Contributors
- Google Summer of Code participant: Dimitrios Katsiros
- Mentor: Kostas Papadimas
- Mentor: Theodoros Karounos
- Mentor: Iraklis Varlamis
- Organization: [GFOSS](https://gfoss.eu/)

## Usage

### Wiki 
An extended documentation has been written in order to the service to be understandable and maintainable. Please check first the [wiki](./wiki) pages.

#### Syntax

```
python3 -m anonymizer

    -i <inputfile>
    
    -o <outputfile>
    
    -f <folder>
    
    -m <method_used(s,strict)/symbol/(lenght==lenght_of_word)>
    
    -p <patterns.json>
    
    -v <verbose_mode>
    
    -w <string of words separated by commas>
    
    -q <quick_mode>
```


#### Defaults

```
python3 -m anonymizer -i testfile.odt -o testfile_anonymized.odt -m s/*/True -p anonymizer/patterns.json
```


#### Explanation

- i: Specify the input's file path.
- o: Specify the output's file  path.
- f: Specify a folder's path. If set, the module will anonymize all .txt and .odt files in the folder.
- m:
    - method: Strict method.
    - symbol: Specify the symbol that will replace sensitive information.
    - length: If True lenght is set to ` len(entity) `, else if a number _n_ is given each entity shall
              be replaced with symbol _n_ times, always respecting the original alignment/format of the text.
- p: Specify the patterns file. A default pattern file is given in _anonymizer/patterns.json_
- v: If typed, verbose mode is on. In verbose mode all identified entities are printed on the console.
- w: If typed the parser expects a string with words separated by commas (,). Each word is anonymized in the text, adding         flexibility to the service. Therefore the user can anonymize words that may not have been identified by default.
- q: If typed, quick mode is on. In quick mode the service only searches for entities given by user through the -w input.
    This is useful in cases where a text has already been parsed and user wants to anonymize additional entities.

## Technologies used

#### Anonymizer Service
 The anonymizer service uses the following libraries: [argparse](https://docs.python.org/3/library/argparse.html), [json](https://docs.python.org/3/library/json.html), [termcolor](https://pypi.org/project/termcolor/).
#### Web GUI
 The web GUI uses the following libraries: [django](https://www.djangoproject.com/), [bootstrap](https://getbootstrap.com/), [requests](https://pypi.org/project/requests/), [crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/install.html), [django-form-utils](https://pypi.org/project/django-form-utils/).
#### LibreOffice Extension
The libreoffice extension uses the following libraries: [uno](https://wiki.openoffice.org/wiki/Uno), [json](https://docs.python.org/3/library/json.html), [pynput](https://pypi.org/project/pynput/).
 
## License
This project is open source as a part of the Google Summer of Code Program. Here, the MIT license is adopted. For more information see LICENSE.
