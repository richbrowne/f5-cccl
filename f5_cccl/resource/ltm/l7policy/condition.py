"""Provides a class for managing BIG-IP L7 Rule Action resources."""
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


class Condition(Resource):
    """L7 Rule Action class."""
    # The property names class attribute defines the names of the
    # properties that we wish to compare.
    properties = dict(
        name=None,
        index=None,
        request=None,
        equals=None,
        httpHost=False,
        host=False,
        httpUri=False,
        pathSegment=False,
        values=None
    )

    def __init__(self, partition, data):
        super(Condition, self).__init__(data['name'], partition)
        for key in self.properties:
            self._data[key] = data.get(key)

    def __eq__(self, other):
        """Check the equality of the two objects.

        Only compare the properties as defined in the
        properties class dictionany.
        """
        if not isinstance(other, Condition):
            return False

        return super(Condition, self).__eq__(other)

    def __str__(self):
        return str(self._data)

    def _uri_path(self, bigip):
        raise NotImplementedError
