# -*- coding: utf-8 -*-
from os.path import realpath

import uno
import unohelper
import pyuno
from com.sun.star.bridge import XUnoUrlResolver
from com.sun.star.frame import XDesktop
from com.sun.star.lang import XComponent
from com.sun.star.reflection import XIdlReflection
from com.sun.star.uno import XComponentContext
from com.sun.star.uno import XInterface

from unotools.datatypes import Sequence
from unotools.utils import cached_property
from unotools.utils import convert_lowercase_to_camecase
from unotools.utils import get_annotation_to_kwargs
from unotools.utils import set_kwargs


class Base:

    def __getattr__(self, name: str) -> XInterface:
        if self.raw is not None:
            return getattr(self.raw, convert_lowercase_to_camecase(name))
        raise AttributeError

    def _show_attributes(self):
        from pprint import pprint
        pprint(dir(self.raw))


class ContextBase(Base, unohelper.Base):

    def __init__(self, context=None):
        self.raw = uno.getComponentContext() if context is None else context
        self.service_manager = self.raw.getServiceManager()
        self.core_reflection = self.create_core_reflection(self.raw)

    def as_raw(self) -> XComponentContext:
        return self.raw

    def create_instance(self, name: str) -> XInterface:
        return self.service_manager.createInstance(name)

    def create_instance_with_context(self, name: str,
                                     context: XComponentContext
                                     ) -> XInterface:
        return self.service_manager.createInstanceWithContext(name, context)

    def create_resolver(self, context: XComponentContext) -> XUnoUrlResolver:
        service_name = 'com.sun.star.bridge.UnoUrlResolver'
        return self.create_instance_with_context(service_name, context)

    def create_core_reflection(self, context: XComponentContext
                               ) -> XIdlReflection:
        service_name = 'com.sun.star.reflection.CoreReflection'
        return self.create_instance_with_context(service_name, context)

    def create_desktop(self, context: XComponentContext) -> XDesktop:
        service_name = 'com.sun.star.frame.Desktop'
        return self.create_instance_with_context(service_name, context)

    @cached_property
    def document(self, context: XComponentContext) -> XComponent:
        return self.create_desktop(context).getCurrentComponent()

    def create_simple_file_access(self, context: XComponentContext
                                  ) -> XIdlReflection:
        service_name = 'com.sun.star.ucb.SimpleFileAccess'
        return self.create_instance_with_context(service_name, context)

    def create_struct(self, type_name: str) -> uno.Any:
        rv, struct = self.core_reflection.forName(type_name).createObject(None)
        return struct

    def make_struct_data(self, type_name: str, **kwargs) -> uno.Any:
        struct = self.create_struct(type_name)
        set_kwargs(struct, kwargs)
        return struct

    def make_point(self, x: int, y: int) -> uno.Any:
        kwargs = self._get_kwargs('make_point', locals())
        return self.make_struct_data('com.sun.star.awt.Point', **kwargs)

    def make_property_value(self, name: str=None, value: str=None,
                            handle: int=None, state: object=None
                            ) -> uno.Any:
        type_name = 'com.sun.star.beans.PropertyValue'
        kwargs = self._get_kwargs('make_property_value', locals())
        return self.make_struct_data(type_name, **kwargs)

    def make_rectangle(self, x: int, y: int, width: int, height: int
                       ) -> uno.Any:
        kwargs = self._get_kwargs('make_rectangle', locals())
        return self.make_struct_data('com.sun.star.awt.Rectangle', **kwargs)

    def make_size(self, width: int, height: int) -> uno.Any:
        kwargs = self._get_kwargs('make_size', locals())
        return self.make_struct_data('com.sun.star.awt.Size', **kwargs)

    def _get_kwargs(self, func_name: str, values: dict) -> dict:
        return get_annotation_to_kwargs(self.__class__, func_name, values)


class ComponentBase(Base):

    def __init__(self, context: XComponentContext, component: XComponent):
        self.context = context
        self.raw = component

    def as_raw(self) -> XComponent:
        return self.raw

    def store_as_url(self, url: str, *values):
        self.raw.storeAsURL(url, self._get_property_values(*values))

    def store_to_url(self, url: str, *values):
        self.raw.storeToURL(url, self._get_property_values(*values))

    def _get_property_values(self, *values) -> Sequence:
        if len(values) == 1 and values[0] is None:
            return Sequence()
        else:
            return Sequence(self.context.make_property_value(*values))


class LoadingComponentBase(ComponentBase):

    def __init__(self, context: XComponentContext,
                 url: str=None,
                 target_frame_name: str='_blank',
                 search_flags: int=0,
                 arguments: tuple=()):
        self.context = context
        self.desktop = self.context.create_desktop(self.context.raw)
        self.url = url if url is not None else self.URL
        self.raw = self.desktop.loadComponentFromURL(self.url,
                                                     target_frame_name,
                                                     search_flags, arguments)


# alias
def constant(name: str) -> object:
    """
    >>> constant('com.sun.star.util.NumberFormat.DATE')
    2
    """
    return pyuno.getConstantByName(name)


def unotype(name: str) -> uno.Type:
    """
    >>> unotype('com.sun.star.uno.XInterface') # doctest: +NORMALIZE_WHITESPACE
    <Type instance com.sun.star.uno.XInterface
        (<uno.Enum com.sun.star.uno.TypeClass ('INTERFACE')>)>
    """
    return pyuno.getTypeByName(name)


def unoclass(name: str) -> type:
    """
    >>> unoclass('com.sun.star.text.XText')
    <class 'uno.com.sun.star.text.XText'>
    """
    return pyuno.getClass(name)


def convert_path_to_url(path: str) -> str:
    """
    >>> convert_path_to_url('/var/tmp/libreoffice')
    'file:///var/tmp/libreoffice'
    """
    return pyuno.systemPathToFileUrl(realpath(path))


def convert_url_to_path(url: str) -> str:
    """
    >>> convert_url_to_path('file:///var/tmp/libreoffice')
    '/var/tmp/libreoffice'
    """
    return pyuno.fileUrlToSystemPath(url)
