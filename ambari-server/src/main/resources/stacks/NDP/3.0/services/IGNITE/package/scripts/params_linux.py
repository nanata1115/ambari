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
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.expect import expect
from resource_management.libraries.functions.stack_features import get_stack_feature_version
from resource_management.libraries.script.script import Script

# server configurations
config = Script.get_config()
exec_tmp_dir = Script.get_tmp_dir()
sudo = AMBARI_SUDO_BINARY
ignite_user = "ignite"
agent_stack_retry_on_unavailability = config['ambariLevelParams']['agent_stack_retry_on_unavailability']
agent_stack_retry_count = expect("/ambariLevelParams/agent_stack_retry_count", int)
version = default("/commandParams/version", None)

# get the correct version to use for checking stack features
version_for_stack_feature_checks = get_stack_feature_version(config)

ignite_conf_dir = "/usr/ndp/{0}/apache-ignite/config".format(version_for_stack_feature_checks)
ignite_home = "/usr/ndp/{0}/apache-ignite".format(version_for_stack_feature_checks)

ignite_conf = {}
ignite_conf.update(config['configurations']['ignite-conf'])

ignite_port = ignite_conf['clientConnectorConfiguration.port']

if 'zoo.cfg' in config['configurations'] and 'clientPort' in config['configurations']['zoo.cfg']:
    cluster_zookeeper_clientPort = config['configurations']['zoo.cfg']['clientPort']
else:
    cluster_zookeeper_clientPort = '2181'

zk_quorum = ""
if 'zookeeper_server_hosts' in config['clusterHostInfo']:
    for host in config['clusterHostInfo']['zookeeper_server_hosts']:
        if zk_quorum:
            zk_quorum += ','
        zk_quorum += host + ":" + str(cluster_zookeeper_clientPort)

ignite_conf['zkConnectionString'] = zk_quorum
