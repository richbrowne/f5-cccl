#!/usr/bin/env python
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
from f5_cccl import bigip
from f5.bigip import ManagementRoot
import json
from mock import Mock, patch
import pytest


class MockNode():
    """A mock BIG-IP node."""

    def __init__(self, name, **kwargs):
        """Initialize the object."""
        self.name = name
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.raw = self.__dict__

    def modify(self, **kwargs):
        """Placeholder: This will be mocked."""
        pass

    def update(self, **kwargs):
        """Placeholder: This will be mocked."""
        pass

    def create(self, partition=None, name=None, **kwargs):
        """Create the node object."""
        pass

    def delete(self):
        """Delete the node object."""
        pass

    def load(self, name=None, partition=None):
        """Load the node object."""
        return MockNode(name)


class Pool():
    """A mock BIG-IP Pool."""

    def __init__(self, name, **kwargs):
        """Initialize the object."""
        self.name = name
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.raw = self.__dict__

    def modify(self, **kwargs):
        """Placeholder: This will be mocked."""
        pass

    def update(self, **kwargs):
        """Placeholder: This will be mocked."""
        pass

    def create(self, partition=None, name=None, **kwargs):
        """Create the pool object."""
        pass

    def delete(self):
        """Delete the pool object."""
        pass

    def load(self, name=None, partition=None):
        """Load the pool object."""
        return Pool(name)


class Policy():
    """A mock BIG-IP Policy."""

    def __init__(self, name, **kwargs):
        """Initialize the object."""
        self.name = name
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.raw = self.__dict__

    def modify(self, **kwargs):
        """Placeholder: This will be mocked."""
        pass

    def update(self, **kwargs):
        """Placeholder: This will be mocked."""
        pass

    def create(self, partition=None, name=None, **kwargs):
        """Create the policy object."""
        pass

    def delete(self):
        """Delete the policy object."""
        pass

    def load(self, name=None, partition=None):
        """Load the policy object."""
        return Policy(name)


class Member():
    """A mock BIG-IP Pool Member."""

    def __init__(self, name, **kwargs):
        """Initialize the object."""
        self.name = name
        self.session = kwargs.get('session', None)
        if kwargs.get('state', None) == 'user-up':
            self.state = 'up'
        else:
            self.state = 'user-down'

    def modify(self, **kwargs):
        """Placeholder: This will be mocked."""
        pass


class Profiles():
    """A container of Virtual Server Profiles."""

    def __init__(self, **kwargs):
        """Initialize the object."""
        self.profiles = kwargs.get('profiles', [])

    def exists(self, name, partition):
        """Check for the existance of a profile."""
        for p in self.profiles:
            if p['name'] == name and p['partition'] == partition:
                return True

        return False

    def create(self, name, partition):
        """Placeholder: This will be mocked."""
        pass


class ProfileSet():
    """A set of Virtual Server Profiles."""

    def __init__(self, **kwargs):
        """Initialize the object."""
        self.profiles = Profiles(**kwargs)


class Policies():
    """A container of Virtual Server Policies."""

    def __init__(self, **kwargs):
        """Initialize the object."""
        self.policies = kwargs.get('policies', [])

    def exists(self, name, partition):
        """Check for the existance of a policy."""
        for p in self.policies:
            if p['name'] == name and p['partition'] == partition:
                return True

        return False

    def create(self, name, partition):
        """Placeholder: This will be mocked."""
        pass


class PolicySet():
    """A set of Virtual Server Policies."""

    def __init__(self, **kwargs):
        """Initialize the object."""
        self.policies = Policies(**kwargs)


class Virtual():
    """A mock BIG-IP Virtual Server."""

    def __init__(self, name, **kwargs):
        """Initialize the object."""
        self.profiles_s = ProfileSet(**kwargs)
        self.policies_s = PolicySet(**kwargs)
        self.name = name
        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.raw = self.__dict__

    def modify(self, **kwargs):
        """Placeholder: This will be mocked."""
        pass

    def create(self, name=None, partition=None, **kwargs):
        """Create the virtual object."""
        pass

    def delete(self):
        """Delete the virtual object."""
        pass

    def load(self, name=None, partition=None):
        """Load the virtual object."""
        return Virtual(name) 


class HealthCheck():
    """A mock BIG-IP Health Monitor."""

    def __init__(self, name, **kwargs):
        """Initialize the object."""
        self.name = name
        self.interval = kwargs.get('interval', None)
        self.timeout = kwargs.get('timeout', None)
        self.send = kwargs.get('send', None)
        self.partition = kwargs.get('partition', None)

    def modify(self, **kwargs):
        """Placeholder: This will be mocked."""
        pass

    def delete(self):
        """Delete the healthcheck object."""
        pass


class VxLANTunnel():
    """A mock BIG-IP VxLAN tunnel."""

    def __init__(self, partition, name, initial_records):
        """Initialize the object."""
        self.partition = partition
        self.name = name
        self.records = initial_records

    def update(self, **kwargs):
        """Update list of vxlan records."""
        self.records = []
        if 'records' in kwargs:
            self.records = kwargs['records']


class MockService():
    """A mock Services service object."""

    def __init__(self):
        """Initialize the object."""
        pass

    def load(self, name, partition):
        """Load a mock iapp."""
        return MockService()

    def create(self, name=None, template=None, partition=None, variables=None,
               tables=None, trafficGroup=None, description=None):
        """Create a mock iapp."""
        pass

    def update(self, **properties):
        """Update a mock iapp."""
        pass

    def delete(self):
        """Delete the iapp object."""
        pass


class MockServices():
    """A mock Application services object."""

    def __init__(self):
        """Initialize the object."""
        self.service = MockService()

    def get_collection(self):
        """Get collection of iapps."""
        return []


class MockApplication():
    """A mock Sys application object."""

    def __init__(self):
        """Initialize the object."""
        self.services = MockServices()


class MockFolders():
    """A mock Sys folders object."""

    def __init__(self):
        """Initialize the object."""

    def get_collection():
        """Get collection of partitions."""
        pass


class MockSys():
    """A mock BIG-IP sys object."""

    def __init__(self):
        """Initialize the object."""
        self.application = MockApplication()
        self.folders = MockFolders()


class Iapp():
    """A mock BIG-IP iapp object."""

    def __init__(self, name=None, **kwargs):
        """Initialize the object."""
        self.name = name
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.raw = self.__dict__

    def delete(self):
        """Mock delete method."""
        pass

    def update(self, executeAction=None, name=None, partition=None,
               variables=None, tables=None, **kwargs):
        """Mock update method."""
        pass


class MockFolder():
    """A mock BIG-IP folder object."""

    def __init__(self, name):
        """Initialize the object."""
        self.name = name


class MockHttp():
    """A mock Https http object."""

    def __init__(self):
        """Initialize the object."""

    def create(self, partition=None, **kwargs):
        """Create a http healthcheck object."""
        pass

    def load(self, name=None, partition=None):
        """Load a http healthcheck object."""
        return MockHttp() 


class MockHttps():
    """A mock Monitor https object."""

    def __init__(self):
        """Initialize the object."""
        self.http = MockHttp()

    def get_collection(self):
        """Get collection of http healthchecks."""
        return []


class MockTcp():
    """A mock Tcps tcp object."""

    def __init__(self):
        """Initialize the object."""
        pass

    def create(self, partition=None, **kwargs):
        """Create a tcp healthcheck object."""
        pass

    def load(self, name=None, partition=None):
        """Load a tcp healthcheck object."""
        return MockTcp() 


class MockTcps():
    """A mock Monitor tcps object."""

    def __init__(self):
        """Initialize the object."""
        self.tcp = MockTcp()

    def get_collection(self):
        """Get collection of tcp healthchecks."""
        return []


class MockIcmp():
    """A mock Icmps tcp object."""

    def __init__(self):
        """Initialize the object."""
        pass

    def create(self, partition=None, **kwargs):
        """Create a tcp healthcheck object."""
        pass

    def load(self, name=None, partition=None):
        """Load a tcp healthcheck object."""
        return MockIcmp()


class MockIcmps():
    """A mock Monitor tcps object."""

    def __init__(self):
        """Initialize the object."""
        self.gateway_icmp = MockIcmp()

    def get_collection(self):
        """Get collection of tcp healthchecks."""
        return []


class MockHttpS():
    """A mock Icmps tcp object."""

    def __init__(self):
        """Initialize the object."""
        pass

    def create(self, partition=None, **kwargs):
        """Create a tcp healthcheck object."""
        pass

    def load(self, name=None, partition=None):
        """Load a tcp healthcheck object."""
        return MockHttpS()


class MockHttpSs():
    """A mock Monitor tcps object."""

    def __init__(self):
        """Initialize the object."""
        self.https = MockHttpS()

    def get_collection(self):
        """Get collection of tcp healthchecks."""
        pass


class MockMonitor():
    """A mock Ltm monitor object."""

    def __init__(self):
        """Initialize the object."""
        self.https = MockHttps()
        self.tcps = MockTcps()
        self.https_s = MockHttpSs()
        self.gateway_icmps = MockIcmps()

class MockVirtuals():
    """A mock Ltm virtuals object."""

    def __init__(self):
        """Initialize the object."""
        self.virtual = Virtual('test')

    def get_collection(self):
        """Get collection of virtuals."""
        pass


class MockPools():
    """A mock Ltm pools object."""

    def __init__(self):
        """Initialize the object."""
        self.pool = Pool('test')

    def get_collection(self):
        """Get collection of pools."""
        pass


class MockPolicys():
    """A mock Ltm policy object."""

    def __init__(self):
        """Initialize the object."""
        self.policy = Policy('test')

    def get_collection(self):
        """Get collection of policies."""
        pass


class MockNodes():
    """A mock Ltm nodes object."""

    def __init__(self):
        """Initialize the object."""
        self.node = MockNode('test')

    def get_collection(self):
        """Get collection of nodes."""
        pass


class MockLtm():
    """A mock BIG-IP ltm object."""

    def __init__(self):
        """Initialize the object."""
        self.monitor = MockMonitor()
        self.virtuals = MockVirtuals()
        self.pools = MockPools()
        self.nodes = MockNodes()
        self.policys = MockPolicys()


class MockTm():
    def __init__(self):
        self.ltm = MockLtm()
        self.sys = MockSys()


class MockHealthMonitor():
    """A mock BIG-IP healthmonitor object."""

    def __init__(self, name, partition):
        """Initialize the object."""
        self.name = name
        self.partition = partition


class BigIPTest(bigip.CommonBigIP):
    """BIG-IP configuration tests.

    Test BIG-IP configuration given various cloud states and existing
    BIG-IP states
    """

    def create_mock_pool(self, name, **kwargs):
        """Create a mock pool server object."""
        pool = Pool(name, **kwargs)
        self.pools[name] = pool
        pool.modify = Mock()
        return pool

    def create_mock_pool_member(self, name, **kwargs):
        """Create a mock pool member object."""
        member = Member(name, **kwargs)
        self.members[name] = member
        member.modify = Mock()
        return member

    def mock_virtuals_get_collection(self, requests_params=None):
        """Mock: Return a mocked collection of virtuals."""
        virtuals = []
        for v in self.bigip_data['virtuals']:
            virtual = Virtual(**v)
            virtuals.append(virtual)

        return virtuals

    def mock_pools_get_collection(self, requests_params=None):
        """Mock: Return a mocked collection of pools."""
        pools = []
        for p in self.bigip_data['pools']:
            pool = Pool(**p)
            pools.append(pool)

        return pools

    def mock_policys_get_collection(self, requests_params=None):
        """Mock: Return a mocked collection of policies."""
        policies = []
        for p in self.bigip_data['policies']:
            policy = Policy(**p)
            policies.append(policy)

        return policies

    def mock_iapps_get_collection(self, requests_params=None):
        """Mock: Return a mocked collection of app svcs."""
        iapps = []
        for i in self.bigip_data['iapps']:
            iapp = Iapp(**i)
            iapps.append(iapp)

        return iapps

    def mock_monitors_get_collection(self, requests_params=None):
        monitors = []
        return monitors

    def mock_nodes_get_collection(self, requests_params=None):
        """Mock: Return a mocked collection of nodes."""
        nodes = []
        for n in self.bigip_data['nodes']:
            node = MockNode(**n)
            nodes.append(node)

        return nodes

    def read_test_data(self, bigip_state):
        """Read test data for the Big-IP state."""
        # Read the BIG-IP state
        with open(bigip_state) as json_data:
            self.bigip_data = json.load(json_data)


@pytest.fixture()
def big_ip():
    """Fixture to supply a mocked BIG-IP."""
    # Mock the call to _get_tmos_version(), which tries to make a
    # connection
    with patch.object(ManagementRoot, '_get_tmos_version'):
        big_ip = BigIPTest('1.2.3.4', 'admin', 'admin', 'test1')

    bigip_state='f5_cccl/test/bigip_data.json'
    big_ip.read_test_data(bigip_state)

    big_ip.tm = MockTm()

    big_ip.tm.ltm.pools.get_collection = \
        Mock(side_effect=big_ip.mock_pools_get_collection)
    big_ip.tm.ltm.policys.get_collection = \
        Mock(side_effect=big_ip.mock_policys_get_collection)
    big_ip.tm.ltm.virtuals.get_collection = \
        Mock(side_effect=big_ip.mock_virtuals_get_collection)
    big_ip.tm.ltm.monitor.https.get_collection = \
        Mock(side_effect=big_ip.mock_monitors_get_collection)
    big_ip.tm.ltm.monitor.https_s.get_collection = \
        Mock(side_effect=big_ip.mock_monitors_get_collection)
    big_ip.tm.ltm.monitor.tcps.get_collection = \
        Mock(side_effect=big_ip.mock_monitors_get_collection)
    big_ip.tm.ltm.monitor.gateway_icmps.get_collection = \
        Mock(side_effect=big_ip.mock_monitors_get_collection)
    big_ip.tm.sys.application.services.get_collection = \
        Mock(side_effect=big_ip.mock_iapps_get_collection)
    big_ip.tm.ltm.nodes.get_collection = \
        Mock(side_effect=big_ip.mock_nodes_get_collection)

    return big_ip
