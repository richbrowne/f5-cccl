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
        request=True,

        equals=None,
        endsWith=None,        
        startsWith=None,
        contains=None,

        negate=False,
        missing=False,

        httpHost=False,
        host=False,
        
        httpUri=False,
        pathSegment=False,
        path=False
        extension=False        

        httpHeader=False,
        httpCookie=False,

        tmName=None
        values=None
    )

    def __init__(self, name, match_type, data):
        super(Condition, self).__init__(name, partition=None)

        self._data['request'] = True

        self.match_type = 
        value = data.get('values', list())
        tm_name = data.get('tmName', None)

        if data.get('httpHost', False):
            condition_map = {'httpHost': True, 'host': True, 'values': value}
        elif data.get('httpUri', False):
            condition_map = {'httpUri': True, 'path': True, 'values': value}
            if data.get('path', False):
                condition_map['path'] = True
            elif data.get('pathSegment', False):
                condition_map['pathSegment'] = True
            elif data.get('extension', False):
                condition_map['extension'] = True
            else:
                print("must specify one of path, pathSegment, or extension "
                      "for HTTP URI matching condition")
        elif data.get('httpHeader', False):
            condition_map = {'httpHeader': True, 'tmName': tm_name, 'values': value}
        elif data.get('httpCookie', False):
            condition_map = {'httpCookie': True, 'tmName': tm_name, 'values': value}            
        else:
            print("Invalid match type must be one of: httpHost, httpUri, "
                  "httpHeader, or httpCookie")

        condition_map 
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
        """Return the URI path of an rule object.

        Not implemented because the current implementation does
        not manage Rules individually."""
        raise NotImplementedError
