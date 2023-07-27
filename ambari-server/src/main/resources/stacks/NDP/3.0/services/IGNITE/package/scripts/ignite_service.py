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


class IgniteService(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

    def configure(self, env):
        import params
        params.pika_slave = True
        env.set_params(params)
        File(format(params.ignite_conf_dir + "/default-config.xml"),
             mode=0755,
             content=Template("ignite-conf.xml.j2"),
             owner=params.ignite_user,
             group=params.ignite_user
             )
        File(format(params.ignite_home + "/bin/include/setenv.sh"),
             mode=0755,
             content=Template("setenv.sh.j2"),
             owner=params.ignite_user,
             group=params.ignite_user
             )
        File(format(params.ignite_home + "/bin/include/stop-ignite.sh"),
             mode=0755,
             content=Template("stop-ignite.sh.j2"),
             owner=params.ignite_user,
             group=params.ignite_user
             )
        Directory(
            "/var/run/apache-ignite",
            mode=0755,
            cd_access='a',
            owner=params.ignite_user,
            group=params.ignite_user,
            create_parents=True,
            recursive_ownership=True
        )
        Directory(
            "/home/ignite",
            mode=0755,
            cd_access='a',
            owner=params.ignite_user,
            group=params.ignite_user,
            create_parents=True,
            recursive_ownership=True
        )

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

        no_op_test = format("ls /var/run/apache-ignite/ignite.pid >/dev/null 2>&1 && ps `cat /var/run/apache-ignite/ignite.pid` | grep `cat /var/run/apache-ignite/ignite.pid` >/dev/null 2>&1")

        start_cmd = format("sh " + params.ignite_home + "/bin/ignite.sh "+params.ignite_conf_dir+"/default-config.xml & echo $! >> /var/run/apache-ignite/ignite.pid;")
        Execute(start_cmd, user=params.ignite_user, not_if=no_op_test)
        active_cmd = format("sleep 10s;sh " + params.ignite_home + "/bin/control.sh --set-state active --yes ")
        Execute(active_cmd, user=params.ignite_user)

    def stop(self, env):
        import params
        env.set_params(params)
        stop_cmd = format("sh "+params.ignite_home + "/bin/include/stop-ignite.sh")
        Execute(stop_cmd, user=params.ignite_user)
        time.sleep(5)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status("/var/run/apache-ignite/ignite.pid")


if __name__ == "__main__":
    IgniteService().execute()
