# -*- coding: UTF-8 -*-
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

from resource_management import *

def dolphin_env():
    import params # import 导入params.
    Directory(params.dolphin_common_map['data.basedir.path'],
              mode=0777,
              owner=params.dolphin_user,
              group=params.dolphin_group,
              create_parents=True
              )

    # 做配置文件的覆盖
    File(format(params.dolphin_env_path), # File表示执行文件操作
         mode=0777,
         content=InlineTemplate(params.dolphin_env_content),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )

    File(format(params.dolphin_bin_dir + "/dolphinscheduler-daemon.sh"),
               mode=0755,
               content=Template("dolphin-daemon.sh.j2"),
               owner=params.dolphin_user,
               group=params.dolphin_group
               )

    File(format(params.dolphin_home + "/master-server/conf/application.yaml"),
         mode=0755,
         content=Template("application-master.yaml.j2"),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )

    File(format(params.dolphin_home + "/worker-server/conf/application.yaml"),
         mode=0755,
         content=Template("application-worker.yaml.j2"),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )

    File(format(params.dolphin_home + "/api-server/conf/application.yaml"),
         mode=0755,
         content=Template("application-api.yaml.j2"),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )

    File(format(params.dolphin_home + "/alert-server/conf/application.yaml"),
         mode=0755,
         content=Template("application-alert.yaml.j2"),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )

    File(format(params.dolphin_home + "/tools/conf/application.yaml"),
         mode=0755,
         content=Template("application-tools.yaml.j2"),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )

    File(format(params.dolphin_home + "/master-server/conf/common.properties"),
         mode=0755,
         content=Template("common.properties.j2"),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )
    File(format(params.dolphin_home + "/tools/conf/common.properties"),
         mode=0755,
         content=Template("common.properties.j2"),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )
    File(format(params.dolphin_home + "/worker-server/conf/common.properties"),
         mode=0755,
         content=Template("common.properties.j2"),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )
    File(format(params.dolphin_home + "/api-server/conf/common.properties"),
         mode=0755,
         content=Template("common.properties.j2"),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )
    File(format(params.dolphin_home + "/alert-server/conf/common.properties"),
         mode=0755,
         content=Template("common.properties.j2"),
         owner=params.dolphin_user,
         group=params.dolphin_group
         )