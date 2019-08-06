# unotools

UnoTools allows you to interact with OpenOffice.org/LibreOffice using
the "UNO bridge". The aim is to make handling OpenDocument easy than
using the original UNO/PyUNO for scripting.

The unotools is quite simple, but you ought to understand UNO APIs.

* [The Apache OpenOffice API Document](http://www.openoffice.org/api/)
* [UNO](https://wiki.openoffice.org/wiki/Uno)
* [PyUNO](https://wiki.openoffice.org/wiki/Python)

There're other tools.

* [pyoo](https://pypi.python.org/pypi/pyoo)
* [unoconv](https://pypi.python.org/pypi/unoconv)

Here are some examples of projects using unotools.

* [odtmanagement](https://bitbucket.org/bastien_roques/odtmanagement)


## How to install

### Requirements

* OpenOffice.org/LibreOffice 3.4 or lator
* Python 3.3 or lator

### On Ubuntu 14.04 

Install libreoffice, uno library and python3:

```bash
$ sudo aptitude install -y libreoffice libreoffice-script-provider-python uno-libs3 python3-uno python3
```

I like virtualenvwrapper to make temporary environment:

```bash
$ sudo aptitude install -y virtualenvwrapper
$ mkvirtualenv -p /usr/bin/python3.4 --system-site-packages tmp3
```

Confirm importing uno module:

```bash
(tmp3)$ python 
Python 3.4.0 (default, Apr 11 2014, 13:05:11) 
[GCC 4.8.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import uno
```

Install unotools from PyPI:

```bash
(tmp3)$ pip install unotools
```

### On Mac OS X

Download LibreOffice DMG package from https://www.libreoffice.org/ and install.

```bash
$ hg clone ssh://hg@bitbucket.org/t2y/unotools
```

In Python 3.3 case, need singledispatch package.
Confirm Python interpreter version included in LibreOffice.

```bash
$ hg clone ssh://hg@bitbucket.org/ambv/singledispatch
```

Set *PYTHONPATH* to resolve additional packages in LibreOffice's
Python interpreter.

```bash
$ export PYTHONPATH="/path/to/singledispatch/:/path/to/unotools/"
```

On Mac OS X, soffice and python commands are as below.

```bash
$ /Applications/LibreOffice.app/Contents/MacOS/soffice --version
LibreOffice 4.4.0.3 de093506bcdc5fafd9023ee680b8c60e3e0645d7
```

Confirm importing unotools package:

```bash
$ /Applications/LibreOffice.app/Contents/MacOS/python
Python 3.3.5 (default, Jan 22 2015, 17:12:45) 
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.51)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import unotools
```

## How to use (on Ubuntu 14.04)

Startup libreoffice:

```bash
(tmp3)$ soffice --accept='socket,host=localhost,port=8100;urp;StarOffice.Service'
```

Download sample-scripts from https://bitbucket.org/t2y/unotools/raw/default/sample-scripts:

```bash
(tmp3)$ python sample-scripts/writer-sample1.py -s localhost
(tmp3)$ python sample-scripts/calc-sample1.py -s localhost -d sample-scripts/datadir/
(tmp3)$ ls
sample-calc.html  sample-calc.pdf  sample-calc_html_eaf26d01.png
sample-scripts  sample-writer.html  sample-writer.pdf
sample.csv  sample.doc  sample.ods  sample.odt  sample.xls
```

There's a sample script to convert odt/ods to pdf.

```bash
(tmp3)$ python sample-scripts/pdf-convert-sample1.py -s localhost -f sample.odt
(tmp3)$ python sample-scripts/pdf-convert-sample1.py -s localhost -f sample.ods
(tmp3)$ ls sample.pdf
```

Look through these sample script, then it help you how to use unotools.


## Interact with interpreter step by step

Interacting documents with UNO make you learn how to use unotools.

Startup LibreOffice:

```bash
$ soffice --accept='socket,host=localhost,port=8100;urp;StarOffice.Service'
```

```python
>>> from unotools import Socket, connect
>>> from unotools.component.writer import Writer
>>> context = connect(Socket('localhost', 8100))
>>> writer = Writer(context)
```

Now, you can see new document window on LibreOffice.

```python
>>> writer.set_string_to_end('Hello\n')
>>> writer.set_string_to_end('World\n')
```

Then, *Hello* and *World* are put into the document window.

```python
>>> text = writer.text
>>> text
<unotools.component.writer.Text object at 0x1064a8e10>
```

Writer inherits
[XTextRange](http://www.openoffice.org/api/docs/common/ref/com/sun/star/text/XTextRange.html)
interface and has those methods. To make full use of unotools, you have to
understand UNO APIs.

There's a tip to confirm what methods are exist in the component.
The `_show_attributes()` is a helper method that unotools component inherit.

```python
>>> text._show_attributes()
[ ...
 'getElementType',
 'getEnd',
 'getImplementationId',
 'getImplementationName',
 'getPropertySetInfo',
 'getPropertyValue',
 'getSomething',
 'getStart',
 'getString',
 'getSupportedServiceNames',
 'getText',
 'getTypes',
  ...
]
```

Though these methods are CamelCase, you can also invoke Python style methods.

```python
>>> text.getString()
'Hello\nWorld\n'

>>> text.get_string()
'Hello\nWorld\n'
```

Both are same method and unotools component handles to convert Python style
to original method.

Let's save this document as *odt*.

```python
>>> from unotools.unohelper import convert_path_to_url
>>> url = convert_path_to_url('./test1.odt')
>>> url
'file:///Users/t2y/work/repo/unotools/test1.odt'
>>> writer.store_to_url(url, 'FilterName', 'writer8')
>>> writer.close(True)
```

If you want to read OpenDocument on file system, like this.

```python
>>> writer = Writer(context, convert_path_to_url('./test1.odt'))
```

If you want to pass *PropertyValue* described in
[loadComponentFromURL Method Options](https://wiki.openoffice.org/wiki/Documentation/BASIC_Guide/StarDesktop),
*context* object has a utility method to create it.
Also multiple property values can be passed if needed.

```python
>>> pv1 = context.make_property_value('Hidden', True)
>>> pv1
(com.sun.star.beans.PropertyValue){
    Name = (string)"Hidden",
    Handle = (long)0x0,
    Value = (any){ (boolean)true },
    State = (com.sun.star.beans.PropertyState)DIRECT_VALUE
}
>>> pv2 = context.make_property_value(..., ...)
>>> w = Writer(context, arguments=(pv1, pv2))
```
