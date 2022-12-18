#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from resource_management import *

# config object that holds the configurations declared in the config xml file
config = Script.get_config()
# /usr/ndp
stack_root = Script.get_stack_root()

version = default("/commandParams/version", "3.0")
# /usr/ndp/3.0/azkaban
azkaban_base_dir = os.path.join(stack_root, version, "azkaban")
# /usr/ndp/3.0/azkaban/conf
azkaban_conf_dir = os.path.join(azkaban_base_dir, "conf")

host_info = config['clusterHostInfo']
host_level_params = config['hostLevelParams']

# azkaban user
azkaban_user = "azkaban"
# azkaban group
azkaban_group = "azkaban"

# mysql root password
mysql_root_password = config['configurations']['azkaban-db']['mysql.root.password']
# azkaban user
mysql_azkaban_user = config['configurations']['azkaban-db']['mysql.user']
# azkaban password
mysql_azkaban_password = config['configurations']['azkaban-db']['mysql.password']
# azkaban database
mysql_azkaban_database = config['configurations']['azkaban-db']['mysql.database']
# mysql.host
mysql_host = config['configurations']['azkaban-db']['mysql.host']
# mysql port
mysql_port = config['configurations']['azkaban-db']['mysql.port']
# azkaban sql script
azkaban_sql_script = os.path.join(azkaban_base_dir, "sql/create-all-sql.sql")

# azkaban config
# global content
global_content = config['configurations']['global.properties']['global_content']
# log4j content
log4j_content = config['configurations']['log4j.properties']['log4j_content']
# user content
users_content = config['configurations']['azkaban-users']['users_content']
# executor properties
azkaban_executor_conf = config['configurations']['azkaban-executor.properties']['azkaban_executor_conf']
# web properties
azkaban_web_conf = config['configurations']['azkaban-web.properties']['azkaban_web_conf']

# azkaban common config
azkaban_name = config['configurations']['azkaban.properties']['azkaban.name']
azkaban_label = config['configurations']['azkaban.properties']['azkaban.label']
azkaban_color = config['configurations']['azkaban.properties']['azkaban.color']
default_timezone_id = config['configurations']['azkaban.properties']['default.timezone.id']
velocity_dev_mode = config['configurations']['azkaban.properties']['velocity.dev.mode']
jetty_use_ssl = config['configurations']['azkaban.properties']['jetty.use.ssl']
jetty_maxThreads = config['configurations']['azkaban.properties']['jetty.maxThreads']
jetty_port = config['configurations']['azkaban.properties']['jetty.port']
mail_sender = config['configurations']['azkaban.properties']['mail.sender']
mail_host = config['configurations']['azkaban.properties']['mail.host']
job_failure_email = config['configurations']['azkaban.properties']['job.failure.email']
job_success_email = config['configurations']['azkaban.properties']['job.success.email']
lockdown_create_projects = config['configurations']['azkaban.properties']['lockdown.create.projects']
jetty_connector_stats = config['configurations']['azkaban.properties']['jetty.connector.stats']
executor_connector_stats = config['configurations']['azkaban.properties']['executor.connector.stats']