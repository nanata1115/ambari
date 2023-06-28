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
import time
from resource_management import *


class CrateService(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        with open("/etc/passwd") as f:
            userlist = []
            for line in f:
                line = line.strip()
                vec = line.split(':')
                userlist.append(vec[0])
            if params.crate_user in userlist:
                Logger.info("Crate Deploy User : " + params.crate_user + "already exists ")
            else:
                Execute(('useradd', params.crate_user))
        Execute(('sed -i \'/^' + params.crate_user + '/d\' /etc/sudoers'))
        Execute(('sed -i \'$a' + params.crate_user + '  ALL=(ALL)  NOPASSWD: NOPASSWD: ALL\' /etc/sudoers'))

    def configure(self, env):
        import params
        env.set_params(params)
        Directory('/etc/crate/conf',
                  create_parents=True,
                  mode=0751,
                  owner=params.crate_user,
                  group=params.crate_user)
        Directory(format(params.crate_home + '/logs'),
                  create_parents=True,
                  mode=0751,
                  owner=params.crate_user,
                  group=params.crate_user)
        Directory(params.crate_home,
                  create_parents=True,
                  mode=0751,
                  owner=params.crate_user,
                  group=params.crate_user)
        Directory('/var/run/crate',
                  create_parents=True,
                  mode=0751,
                  owner=params.crate_user,
                  group=params.crate_user)
        Execute(('rm -rf ' + " " + params.crate_home))
        Execute(('ln -s ' + params.crate_path + " " + params.crate_home))
        Execute('rm -rf /etc/crate/conf')
        Execute(('ln -s ' + params.crate_conf_path + " " + '/etc/crate/conf'))
        Execute('sysctl -w vm.max_map_count=262144')
        File(format(params.crate_conf_path + "/crate-env.sh"),  # File表示执行文件操作
             mode=0777,
             content=InlineTemplate(params.crate_env),
             owner=params.crate_user,
             group=params.crate_user
             )
        File(format(params.crate_conf_path + "/crate.yml"),
             mode=0755,
             content=Template("crate.yml.j2"),
             owner=params.crate_user,
             group=params.crate_user
             )
        File(format(params.crate_home + "/bin/crate.sh"),
             mode=0755,
             content=Template("crate.sh.j2"),
             owner=params.crate_user,
             group=params.crate_user
             )

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

        no_op_test = format(
            "ls {crate_pid_path} >/dev/null 2>&1 && ps `cat {crate_pid_path}` | grep `cat {crate_pid_path}` >/dev/null 2>&1")

        start_cmd = format("source " + params.crate_conf_path + "/crate-env.sh ; sh " + params.crate_home
                           + "/bin/crate.sh start")
        Execute(start_cmd, user=params.crate_user, not_if=no_op_test)

    def stop(self, env):
        import params
        env.set_params(params)
        stop_cmd = format("source " + params.crate_conf_path + "/crate-env.sh ; sh " + params.crate_home
                          + "/bin/crate.sh stop")
        Execute(stop_cmd, user=params.crate_user)
        time.sleep(5)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.crate_pid_path)


if __name__ == "__main__":
    CrateService().execute()
