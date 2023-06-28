#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from ambari_commons.constants import AMBARI_SUDO_BINARY
from resource_management.libraries.functions import StackFeature, format
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.expect import expect
from resource_management.libraries.functions.get_architecture import get_architecture
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions.stack_features import get_stack_feature_version
from resource_management.libraries.functions.version import get_major_version, format_stack_version
from resource_management.libraries.script.script import Script

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
sudo = AMBARI_SUDO_BINARY

architecture = get_architecture()

# Needed since this writes out the Atlas Hive Hook config file.
cluster_name = config['clusterName']
serviceName = config['serviceName']
role = config['role']

hostname = config['agentLevelParams']['hostname']

# New Cluster Stack Version that is defined during the RESTART of a Rolling Upgrade
version = default("/commandParams/version", None)
stack_name = default("/clusterLevelParams/stack_name", None)
stack_name_uppercase = stack_name.upper()
upgrade_direction = default("/commandParams/upgrade_direction", None)
agent_stack_retry_on_unavailability = config['ambariLevelParams']['agent_stack_retry_on_unavailability']
agent_stack_retry_count = expect("/ambariLevelParams/agent_stack_retry_count", int)

stack_root = Script.get_stack_root()

stack_version_unformatted = config['clusterLevelParams']['stack_version']
stack_version_formatted = format_stack_version(stack_version_unformatted)
major_stack_version = get_major_version(stack_version_formatted)
version_for_stack_feature_checks = get_stack_feature_version(config)

crate_path = format(stack_root + '/' + stack_version_unformatted + '/crate-5.4.0')
crate_home = format(stack_root + '/current/crate')
crate_conf_path = crate_home + "/config"

crate_hosts = config['clusterHostInfo']['crate_server_hosts']
crate_hosts.sort()

common_params = {}
common_params.update(config['configurations']['common'])
common_params['network.bind_host'] = hostname
common_params['crate_hosts'] = crate_hosts
seed_hosts = ''
for host in crate_hosts:
    seed_hosts = seed_hosts + '\n - ' + host + ':' + common_params['transport.tcp.port']
common_params['discovery.seed_hosts'] = seed_hosts
nodes = len(crate_hosts)
crate_env = config['configurations']['crate-env']['content']
crate_user = 'crate'
crate_pid_path = '/var/run/crate/crate_pid'

# hadoop params
if stack_version_formatted and check_stack_feature(StackFeature.ROLLING_UPGRADE, stack_version_formatted):
    stack_version = None
    upgrade_stack = stack_select._get_upgrade_stack()
    if upgrade_stack is not None and len(upgrade_stack) == 2 and upgrade_stack[1] is not None:
        stack_version = upgrade_stack[1]
