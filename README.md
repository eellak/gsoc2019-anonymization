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
- Complete the implementation of data anonymizer.
- Complete the sensitive data recognition matcher using spaCy in _.txt_ and _.odt_ files.
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
