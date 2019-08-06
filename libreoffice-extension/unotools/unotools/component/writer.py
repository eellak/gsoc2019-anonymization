# -*- coding: utf-8 -*-
from com.sun.star.text import XText
from com.sun.star.text import XTextRange

from unotools.unohelper import ComponentBase
from unotools.unohelper import LoadingComponentBase


class Text(ComponentBase):
    pass


class Writer(LoadingComponentBase):

    URL = 'private:factory/swriter'

    @property
    def text(self) -> XText:
        return Text(self.context, self.raw.getText())

    def get_start(self) -> XTextRange:
        return self.text.getStart()

    def get_end(self) -> XTextRange:
        return self.text.getEnd()

    def set_string_to_start(self, text: str):
        self.get_start().setString(text)

    def set_string_to_end(self, text: str):
        self.get_end().setString(text)
