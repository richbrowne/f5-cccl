"""Provides a class for managing BIG-IP L7 Policy resources."""
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

import f5
from f5_cccl.resource import Resource
from f5_cccl.resource.ltm.l7policy.action import Action
from f5_cccl.resource.ltm.l7policy.condition import Condition
from f5_cccl.resource.ltm.l7policy.rule import Rule


class Policy(Resource):
    """L7 Policy class."""
    # The property names class attribute defines the names of the
    # properties that we wish to compare.
    properties = dict(
        name=None,
        partition=None,
        controls=None,
        strategy=None,
        legacy=True,
        requires=None,
        rules=None
    )

    def __init__(self, data):
        """Create the policy and nested class objects"""
        if isinstance(data, f5.bigip.tm.ltm.policy.Policy):
            data = self._flatten_policy(data)
        super(Policy, self).__init__(data['name'], data['partition'])
        for key, value in self.properties.items():
            if key == 'rules':
                self._data[key] = self._create_rules(
                    data['partition'], data[key])
                continue
            if key == 'name' or key == 'partition':
                continue
            self._data[key] = data.get(key, value)

    def __eq__(self, other):
        """Check the equality of the two objects.

        Only compare the properties as defined in the
        properties class dictionany.
        """
        if not isinstance(other, Policy):
            return False

        for key in self.properties:
            if key == 'rules':
                if len(self._data[key]) != len(other.data[key]):
                    # logger.debug('Rule length is unequal')
                    return False
                for index, rule in enumerate(self._data[key]):
                    if rule != other.data[key][index]:
                        return False
                continue
            if self._data[key] != other.data.get(key, None):
                logger.debug(
                    'Policies are unequal, %s does not match: %s - %s',
                    key, self._data[key], other.data.get(key, None))
                return False
        return True

    def __str__(self):
        return str(self._data)

    def _create_rules(self, partition, rules):
        new_rules = []
        for rule in rules:
            new_rules.append(Rule(partition, rule))
        new_rules.sort(key=lambda x: x.data['ordinal'])
        return new_rules

    def _uri_path(self, bigip):
        return bigip.tm.ltm.policy

    def _flatten_policy(self, bigip_policy):
        policy = {}
        for key in Policy.properties:
            if key == 'rules':
                policy['rules'] = self._flatten_rules(
                    bigip_policy.__dict__['rulesReference']['items'])
            elif key == 'legacy':
                policy['legacy'] = True
            else:
                policy[key] = bigip_policy.__dict__.get(key)
        return policy

    def _flatten_rules(self, rules_list):
        rules = []
        for rule in rules_list:
            flat_rule = {}
            for key in Rule.properties:
                if key == 'actions':
                    flat_rule[key] = self._flatten_actions(rule)
                elif key == 'conditions':
                    flat_rule[key] = self._flatten_condition(rule)
                else:
                    flat_rule[key] = rule.get(key)
            rules.append(flat_rule)
        return rules

    def _flatten_actions(self, rule):
        actions = []
        for action in rule['actionsReference']['items']:
            flat_action = {}
            for key in Action.properties:
                flat_action[key] = action.get(key)
            actions.append(flat_action)
        return actions

    def _flatten_condition(self, rule):
        conditions = []
        for condition in rule['conditionsReference']['items']:
            flat_condition = {}
            for key in Condition.properties:
                flat_condition[key] = condition.get(key)
            conditions.append(flat_condition)
        return conditions
