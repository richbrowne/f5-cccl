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
from f5_cccl.resource.ltm.policy.action import Action
from f5_cccl.resource.ltm.policy.condition import Condition


class Rule(Resource):
    """L7 Rule class"""
    # The property names class attribute defines the names of the
    # properties that we wish to compare.
    properties = dict(
        name=None,
        ordinal=0,
        actions=None,
        conditions=None
    )

    def __init__(self, name, partition, **data):
        super(Rule, self).__init__(name, partition)
        self._data['ordinal'] = data.get('ordinal', 0)
        self._data['actions'] = self._create_actions(
            partition, data.get('actions', list()))
        self._data['conditions'] = self._create_conditions(
            partition, data.get('conditions', list()))

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

    def __lt__(self, other):
        return self._data['ordinal'] < other.data['ordinal']

    def _create_actions(self, partition, actions):
        new_actions = []

        for index, action in enumerate(actions):
            new_actions.append(Action(index, partition, action))
        
        return [action.data for action in sorted(new_actions)]

    def _create_conditions(self, partition, conditions):
        new_conditions = [Condition(partition, condition)
                          for condition in conditions]

        return [condition.data for condition in sorted(new_conditions)]


    def _uri_path(self, bigip):
        raise NotImplementedError
