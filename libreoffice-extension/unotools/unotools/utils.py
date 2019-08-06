# -*- coding: utf-8 -*-
import functools
import glob
import os
from os.path import join as pathjoin


def cached_property(func: callable) -> property:
    return property(functools.lru_cache()(func))


def get_annotation_to_kwargs(klass: type, func_name: str, values: dict
                             ) -> dict:
    ann = getattr(klass, func_name).__annotations__
    return {key: values.get(key) for key in ann.keys()
            if values.get(key) is not None}


def set_kwargs(obj: object, kwargs: dict):
    for key, value in kwargs.items():
        if value is not None:
            setattr(obj, key.title(), value)


def convert_lowercase_to_camecase(name: str) -> str:
    """
    >>> convert_lowercase_to_camecase('')
    ''
    >>> convert_lowercase_to_camecase('close')
    'close'
    >>> convert_lowercase_to_camecase('get_title')
    'getTitle'
    >>> convert_lowercase_to_camecase('set_array_value')
    'setArrayValue'
    >>> convert_lowercase_to_camecase('getURL')
    'getURL'
    """
    tokens = name.split('_')
    first, *rest = tokens
    return first + ''.join(i.title() for i in rest)


def get_file_list(path: str) -> str:
    for root, dirs, files in os.walk(path):
        for filename in files:
            yield pathjoin(root, filename)


def search_file(path: str, name: str) -> str:
    for root, dirs, files in os.walk(path):
        for file_path in glob.glob(os.path.join(root, name)):
            yield file_path
