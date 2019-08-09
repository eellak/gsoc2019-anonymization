import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='anonymizer',
    version="0.0.4",
    # scripts=['__init__.py', '__main__.py'],
    author="Dimitris Katsiros",
    author_email="dkatsiros@gmail.com",
    description="Anonymizer Service implemented for GSoC 2019",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eellak/gsoc2019-anonymization",
    # packages=setuptools.find_packages(),
    packages=['anonymizer'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
