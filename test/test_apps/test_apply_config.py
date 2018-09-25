#!/usr/bin/env python

import json
import sys

from f5_cccl import F5CloudServiceManager

def main(argv):

    svcfile = 'f5_cccl/schemas/tests/service.json'
    with open(svcfile, 'r') as fp:
        services = json.loads(fp.read())

    cccl_mgr = F5CloudServiceManager('192.168.1.35',
                                     'admin', 'admin', 'Test')

    cccl_mgr.apply_config(services)
    sys.stdin.readline()
    pool0 = services['pools'][0]
    new_member={"address": "172.16.0.102", "port": 8080, "ratio": 2}
    pool0["members"].append(new_member)

    cccl_mgr.apply_config(services)
    sys.stdin.readline()
    pool0['loadBalancingMode'] = 'ratio-member'
    cccl_mgr.apply_config(services)
    sys.stdin.readline()    
    cccl_mgr.apply_config({})    



if __name__ == '__main__':
    main(sys.argv)
