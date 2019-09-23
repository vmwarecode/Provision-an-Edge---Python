#
# Provision an Edge
# 
# Usage: VC_USERNAME='user@velocloud.net' VC_PASSWORD=s3cret python provision_edge.py
#

import os
from uuid import uuid4

from client import *

# EDIT THESE
VCO_HOSTNAME = 'vco.velocloud.net'
ENTERPRISE_ID = 1 # As may be found e.g. in web UI URL path
TARGET_PROFILE_NAME = "Quick Start Profile"
EDGE_NAME = "API Demo %s" % str(uuid4())

def main():

    client = VcoRequestManager(VCO_HOSTNAME)
    client.authenticate(os.environ['VC_USERNAME'], os.environ['VC_PASSWORD'], is_operator=os.environ.get('VC_OPERATOR', False))


    #
    # 1. Get enterprise profiles
    #
    print('### GETTING ENTERPRISE PROFILES ###')
    profileId = None
    try:
        profiles = client.call_api('enterprise/getEnterpriseConfigurations', {
            'enterpriseId': ENTERPRISE_ID
        })
        target = [p for p in profiles if p['name'] == TARGET_PROFILE_NAME][0]
        profileId = target['id']
    except Exception as e:
        print('Failed to retrieve profile "%s"' % TARGET_PROFILE_NAME)
        print(e)

    #
    # 2. Provision an Edge
    #
    print('### PROVISIONING EDGE ###')
    try:
        client.call_api('edge/edgeProvision', {
            'enterpriseId': ENTERPRISE_ID,
            'name': EDGE_NAME,
            'description': 'A demo Edge generated with a Python API client',
            'modelNumber': 'edge500',
            'configurationId': profileId
        })
    except Exception as e:
        print('Failed to provision Edge "%s"' % EDGE_NAME)
        print(e)

    print('Successfully provisioned Edge %s' % EDGE_NAME)

if __name__ == '__main__':
    main()