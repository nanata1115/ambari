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

import pwd
from resource_management import *


# user exists or not
def azkaban_user_exists():
    import params
    try:
        pwd.getpwnam(params.azkaban_user)
        return True
    except KeyError:
        return False


# executor azkaban sql
def executor_azkaban_sql():
    import params
    # replace
    Execute("sed -i 's/mysql.database/{0}/' {1}".format(params.mysql_azkaban_database, params.azkaban_sql_script))
    Execute("sed -i 's/mysql.user/{0}/' {1}".format(params.mysql_azkaban_user, params.azkaban_sql_script))
    Execute("sed -i 's/mysql.password/{0}/' {1}".format(params.mysql_azkaban_password, params.azkaban_sql_script))
    # exe sql script
    cmd = "{0}/bin/mysql -h{1} -P{2} -uroot -p{3} < {4}".format(params.azkaban_base_dir,
                                                                params.mysql_host,
                                                                params.mysql_port,
                                                                params.mysql_root_password,
                                                                params.azkaban_sql_script)
    Execute(cmd)


# common setup
def common_setup():
    import params
    if not azkaban_user_exists():
        Group(params.azkaban_group, ignore_failures=True)
        User(params.azkaban_user,
             gid=params.azkaban_group,
             groups=[params.azkaban_group],
             ignore_failures=True)
        cmd = format("chown -R {azkaban_user}:{azkaban_group} {azkaban_base_dir}")
        Execute(cmd)

    # global properties
    global_content = InlineTemplate(params.global_content)
    File('{0}/global.properties'.format(params.azkaban_conf_dir),
         content=global_content,
         owner=params.azkaban_user,
         group=params.azkaban_group)
    # log4j properties
    log4j_content = InlineTemplate(params.log4j_content)
    File('{0}/log4j.properties'.format(params.azkaban_conf_dir),
         content=log4j_content,
         owner=params.azkaban_user,
         group=params.azkaban_group)


# web common setup
def web_common_setup():
    import params
    common_setup()
    # azkaban-user.xml
    users_content = InlineTemplate(params.users_content)
    File('{0}/azkaban-users.xml'.format(params.azkaban_conf_dir),
         content=users_content,
         owner=params.azkaban_user,
         group=params.azkaban_group)
    # azkaban.properties
    azkaban_web_conf = InlineTemplate(params.azkaban_web_conf)
    File('{0}/azkaban.properties'.format(params.azkaban_conf_dir),
         content=azkaban_web_conf,
         owner=params.azkaban_user,
         group=params.azkaban_group)
    cmd = format("chown -R {azkaban_user}:{azkaban_group} {azkaban_base_dir}")
    Execute(cmd)


# executor common setup
def executor_common_setup():
    import params
    common_setup()
    # azkaban.properties
    azkaban_executor_conf = InlineTemplate(params.azkaban_executor_conf)
    File('{0}/azkaban.properties'.format(params.azkaban_conf_dir),
         content=azkaban_executor_conf,
         owner=params.azkaban_user,
         group=params.azkaban_group)
    cmd = format("chown -R {azkaban_user}:{azkaban_group} {azkaban_base_dir}")
    Execute(cmd)
