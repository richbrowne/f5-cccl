"""Provides a class for managing BIG-IP L7 Rule resources."""
# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from f5_cccl.resource import Resource
from f5_cccl.resource.ltm.l7policy.action import Action
from f5_cccl.resource.ltm.l7policy.condition import Condition


class Rule(Resource):
    """L7 Rule class"""
    # The property names class attribute defines the names of the
    # properties that we wish to compare.
    properties = dict(
        name=None,
        ordinal=None,
        actions=None,
        conditions=None
    )

    def __init__(self, partition, data):
        super(Rule, self).__init__(data['name'], partition)
        for key in self.properties:
            if key == 'actions':
                self._data[key] = self._create_actions(
                    partition, data[key])
                continue
            if key == 'conditions':
                self._data[key] = self._create_conditions(
                    partition, data[key])
                continue
            if key == 'name':
                continue
            self._data[key] = data.get(key)

    def __eq__(self, other):
        """Check the equality of the two objects.

        Only compare the properties as defined in the
        properties class dictionany.
        """
        if not isinstance(other, Rule):
            return False

        for key in self.properties:
            if key == 'actions' or key == 'conditions':
                if len(self._data[key]) != len(other.data[key]):
                    # logger.debug('%s length is unequal', key)
                    return False
                for index, obj in enumerate(self._data[key]):
                    if obj != other.data[key][index]:
                        return False
                continue
            if self._data[key] != other.data.get(key, None):
                print(
                    'Rules are unequal, %s does not match: %s - %s',
                    key, self._data[key], other.data.get(key, None))
                return False
        return True

    def __str__(self):
        return str(self._data)

    def _create_actions(self, partition, actions):
        new_actions = []
        for action in actions:
            new_actions.append(Action(partition, action))
        return new_actions

    def _create_conditions(self, partition, conditions):
        new_conditions = []
        for condition in conditions:
            new_conditions.append(Condition(partition, condition))
        return new_conditions

    def _uri_path(self, bigip):
        raise NotImplementedError
