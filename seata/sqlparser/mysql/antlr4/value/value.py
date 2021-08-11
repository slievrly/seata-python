#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author jsbxyyx
# @since 1.0
from seata.sqlparser.util.SQLUtil import SQLUtil

class ASTNode:
    pass

class ParameterMarkerValue(ASTNode):

    def __init__(self, value: int):
        self.value = value


class StringLiteralValue(ASTNode):

    def __init__(self, value: str):
        self.value = value[1, -1]


class NumberLiteralValue(ASTNode):

    def __init__(self, value: str):
        try:
            self.value = int(value)
        except Exception as e:
            self.value = float(value)


class OtherLiteralValue(ASTNode):

    def __init__(self, value: str):
        self.value = value


class BooleanLiteralValue(ASTNode):

    def __init__(self, value: str):
        if value is None:
            self.value = None
        else:
            self.value = bool(value)


class IdentifierValue(ASTNode):

    def __init__(self, value: str):
        if value is None:
            self.value = None
        else:
            self.value = SQLUtil.remove_quota(value)


class MySQLIdentifierValue(IdentifierValue):

    def __init__(self, value: str):
        super(MySQLIdentifierValue, self).__init__(value)
        self.quota = "`"
