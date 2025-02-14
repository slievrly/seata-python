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

from seata.core.model.BranchType import BranchType
from seata.rm.datasource.DataSourceResourceManager import DataSourceResourceManager


class DefaultResourceManager:
    _resource_manager = None
    resource_manager_map = {}

    def __init__(self):
        self.resource_manager_map[BranchType.AT] = DataSourceResourceManager.get()

    @classmethod
    def get(cls):
        if cls._resource_manager is None:
            cls._resource_manager = DefaultResourceManager()
        return cls._resource_manager

    def branch_commit(self, branch_type, xid, branch_id, resource_id):
        return self.resource_manager_map[branch_type].branch_commit(branch_type, xid, branch_id, resource_id)

    def branch_rollback(self, branch_type, xid, branch_id, resource_id, application_data):
        return self.resource_manager_map[branch_type].branch_rollback(branch_type, xid, branch_id, resource_id,
                                                                      application_data)

    def branch_register(self, branch_type, resource_id, client_id, xid, application_data, lock_keys):
        return self.resource_manager_map[branch_type].branch_register(branch_type, resource_id, client_id, xid,
                                                                      application_data, lock_keys)

    def branch_report(self, branch_type, xid, branch_id, status, application_data):
        return self.resource_manager_map[branch_type].branch_report(branch_type, xid, branch_id, status,
                                                                    application_data)

    def lock_query(self, branch_type, resource_id, xid, lock_keys):
        return self.resource_manager_map[branch_type].lock_query(branch_type, resource_id, xid, lock_keys)

    def register_resource(self, resource):
        self.resource_manager_map[resource.get_branch_type()].register_resource(resource)

    def unregister_resource(self, resource):
        # TODO
        pass

    def get_manager_resources(self):
        all_resources = {}
        values = self.resource_manager_map.values()
        for rm in values:
            res = rm.get_managed_resources()
            all_resources.update(res)
        return all_resources

    def get_manager_resource(self, branch_type):
        return self.resource_manager_map.get(branch_type)
