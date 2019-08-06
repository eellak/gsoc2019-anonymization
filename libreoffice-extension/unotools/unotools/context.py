# -*- coding: utf-8 -*-
import uno  # pragma: no flakes
from com.sun.star.script.provider import XScriptContext

from unotools.unohelper import ContextBase


class LocalContext(ContextBase):

    def __init__(self, context=None):
        super().__init__(context)
        self.resolver = self.create_resolver(self.raw)


class ScriptContext(ContextBase, XScriptContext):
    pass
