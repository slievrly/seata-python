# -*- coding: utf-8 -*-

"""
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from am.mysql_base import UpdateStatement, Default, Constant

from seata.sqlparser.mysql.antlr4.util.MySQLStatementUtil import MySQLStatementUtil
from seata.sqlparser.mysql.antlr4.value import MySQLValue


class UpdateSetItem:

    def __init__(self, owner=None, column=None, value=None):
        self.owner = owner
        self.column = column
        self.value = value


class MySQLUpdateStatement:

    def __init__(self, ctx: UpdateStatement):
        if not isinstance(ctx, UpdateStatement):
            raise TypeError('ctx type error.' + type(ctx).__name__)
        self.table_name = None
        self.table_alias = None
        self.items = []
        self.where = None
        self.order_by = None
        self.limit = None
        self.__ctx = ctx
        self.parse()

    def parse(self):
        self.__parse_table_name()
        self.__parse_table_alias()
        self.__parse_items()
        self.__parse_where()
        self.__parse_order_by()

    def __parse_table_name(self):
        self.table_name = self.__ctx.tableSource.tableName

    def __parse_table_alias(self):
        self.table_alias = self.__ctx.tableSource.tableAlias

    def __parse_items(self):
        items = []
        for ele_idx, ele in enumerate(self.__ctx.updatedElement):
            if ele.column.owner is not None:
                column = ele.column.value
            else:
                column = ele.column.value

            if isinstance(ele.value, Default):
                value = ele.value.value
            elif isinstance(ele.value, Constant):
                value = MySQLStatementUtil.parse_constant(ele.value)
            else:
                value = MySQLValue.NotSupportValue(type(ele.value))

            items.append(UpdateSetItem(ele.column.owner, column, value))
        self.items = items

    def __parse_where(self):
        self.where = self.__ctx.where

    def __parse_order_by(self):
        self.order_by = self.__ctx.orderBy

    def __parse_limit(self):
        self.limit = self.__ctx.limit
