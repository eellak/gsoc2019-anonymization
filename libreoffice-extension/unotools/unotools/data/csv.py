# -*- coding: utf-8 -*-
import csv
from os.path import basename


class CsvFile:

    def __init__(self, path: str, mode: str='r', encoding: str='utf-8',
                 has_header: bool=False, convert_func: callable=lambda x: x,
                 **kwargs):
        self.path = path
        self.file_name = basename(path)
        self.mode = mode
        self.encoding = encoding
        self.header = None
        self.has_header = has_header
        self.convert_func = convert_func
        self.reader_kwargs = kwargs

    def read(self) -> list:
        with open(self.path, mode=self.mode, encoding=self.encoding) as f:
            reader = csv.reader(f, **self.reader_kwargs)
            if self.has_header:
                self.header = next(reader)
            for data in reader:
                yield list(map(self.convert_func, data))
