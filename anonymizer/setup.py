import setuptools

# setup(
#     # This is the name of your PyPI-package.
#     name='anonymizer',
#     # Update the version number for new releases
#     version='0.1',
#     # The name of your scipt, and also the command you'll be using for calling it
#     scripts=['__main__.py']
# )


# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='anonymizer',
    version="0.0.2",
    # scripts=['__init__.py', '__main__.py'],
    author="Dimitris Katsiros",
    author_email="dkatsiros@gmail.com",
    description="Anonymizer Service for GSoC 2019",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/eellak/gsoc2019-anonymization",
    # packages=setuptools.find_packages(),
    packages=['anonymizer'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
