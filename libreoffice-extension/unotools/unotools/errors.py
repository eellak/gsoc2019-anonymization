# -*- coding: utf-8 -*-


class UnotoolsError(Exception):
    pass


class ConnectionError(UnotoolsError):
    pass


class ArgumentError(UnotoolsError):
    pass
