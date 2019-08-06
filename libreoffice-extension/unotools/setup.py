# -*- coding: utf-8 -*-
import sys
from setuptools import setup


VERSION = '0.3.3'

try:
    import pypandoc
    LONG_DESCRIPTION = '\n'.join([
        pypandoc.convert('README.md', 'rst'),
        pypandoc.convert('CHANGELOG.md', 'rst'),
    ])
except (IOError, ImportError):
    LONG_DESCRIPTION = ''

REQUIRES = []
if sys.version_info < (3, 4):
    REQUIRES.append('singledispatch')

CLASSIFIERS = [
    'License :: OSI Approved :: Apache Software License',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Topic :: Office/Business :: Office Suites',
]

setup(
    name='unotools',
    version=VERSION,
    description='Interacting with OpenOffice.org/LibreOffice using UNO',
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    keywords=['uno', 'pyuno', 'office', 'OOo'],
    author='Tetsuya Morimoto',
    author_email='tetsuya dot morimoto at gmail dot com',
    url='http://bitbucket.org/t2y/unotools',
    license='Apache License 2.0',
    platforms=['unix', 'linux', 'osx'],
    packages=['unotools'],
    include_package_data=True,
    install_requires=REQUIRES,
    tests_require=['tox', 'pytest', 'pytest-pep8', 'pytest-flakes'],
)
