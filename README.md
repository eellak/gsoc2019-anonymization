# Google Summer Of Code 2019 :sunny:

### Anonymisation Through Data Encryption of Sensitive Data in ODT and Text Files in Greek Language

## Problem Statement
Over the past year, great importance has been attached to information anonymisation from governments all around the world. The GDPR defines pseudonymization and the processing of personal data in such a way that the data can no longer be attributed to a specific data subject without the use of additional information. Although the GDPR has been implemented since 2018 no reliable infrastructure exists in Greece to encrypt sensitive documents. It is therefore necessary to develop a product specifically for users of the Greek language that can safely and promptly anonymize their data in order for it to abide to the GDPR.

## Abstract
I propose the creation of a LibreOffice extension as well as a web GUI that will anonymize information in any legal document given. All sensitive information should be easily anonymized through this open-source tool. 

On the subject of the creation of the anonymizer I suggest the following metrics. First of all, given any document the anonymizer should encrypt any greek entity in the file from a standard token vocabulary set. The user will be able to add specific arguments for entities to be anonymized (in addition to the standard ones) and he will be given the option to choose for an additional encryption. I believe that the LibreOffice extension as well as the web GUI should be user-friendly so customizable technologies should be used.

## Timeline
Milestones at the end of each [GSoC phase](https://developers.google.com/open-source/gsoc/timeline):

### June 28, 2019 Phase 1 Evaluation:
- Complete the sensitive data recognition matcher using regular expressions in _.txt_ and _.odt_ files.
- Complete the implementation of the data anonymizer module.
### July 26, 2019 Phase 2 Evaluation:
- Initial Documentation.
- Complete the implementation of Linux application with a web GUI.
- Tackling unexpected delays, fixes, runtime evaluation
### August 26, 2019 Final Evaluation:
- Implementing LibreOffice Extension.
- Completion of relevant documentation.
- Tests

## Contributors
- Google Summer of Code participant: Dimitrios Katsiros
- Mentor: Kostas Papadimas
- Mentor: Theodoros Karounos
- Mentor: Iraklis Varlamis
- Organization: [GFOSS](https://gfoss.eu/)

## Usage

#### Syntax

```
python3 -m anonymizer

    -i <inputfile>
    
    -o <outputfile>
    
    -f <folder>
    
    -m <method_used(s,strict)/symbol/(lenght==lenght_of_word)>
    
    -p <patterns.json>
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
