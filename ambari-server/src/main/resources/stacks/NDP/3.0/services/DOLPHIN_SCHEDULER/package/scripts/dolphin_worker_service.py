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

from dolphin_env import dolphin_env


class DolphinWorkerService(Script):
  def install(self, env):
    import params
    env.set_params(params)
    self.install_packages(env)
    with open("/etc/passwd") as f:
      userlist = []
      for line in f:
        line=line.strip()
        vec =line.split(':')
        userlist.append(vec[0])
      if params.dolphin_user in userlist:
        Logger.info("Dolphin Deploy User : " + params.dolphin_user + "already exists ")
      else:
        Execute(('useradd', params.dolphin_user))
    Execute(('sed -i \'/^' + params.dolphin_user + '/d\' /etc/sudoers'))
    Execute(('sed -i \'$a' + params.dolphin_user + '  ALL=(ALL)  NOPASSWD: NOPASSWD: ALL\' /etc/sudoers'))

  def configure(self, env):
    import params
    params.pika_slave = True
    env.set_params(params)

    Execute(('rm -f ' + " " + params.dolphin_home+"/master-server/conf/core-site.xml"))
    Execute(('ln -s /etc/hadoop/conf/core-site.xml' + " " + params.dolphin_home+"/master-server/conf/core-site.xml"))
    Execute(('rm -f ' + " " + params.dolphin_home+"/master-server/conf/hdfs-site.xml"))
    Execute(('ln -s /etc/hadoop/conf/hdfs-site.xml' + " " + params.dolphin_home+"/master-server/conf/hdfs-site.xml"))
    dolphin_env()
  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)
    no_op_test = format("ls {dolphin_pidfile_dir}/worker-server/pid >/dev/null 2>&1 && ps `cat {dolphin_pidfile_dir}/worker-server/pid` | grep `cat {dolphin_pidfile_dir}/worker-server/pid` >/dev/null 2>&1")
    start_cmd = format("sh " + params.dolphin_bin_dir + "/dolphinscheduler-daemon.sh start worker-server")
    Execute(start_cmd, user=params.dolphin_user, not_if=no_op_test)

  def stop(self, env):
    import params
    env.set_params(params)
    stop_cmd = format("sh " + params.dolphin_bin_dir + "/dolphinscheduler-daemon.sh stop worker-server")
    Execute(stop_cmd, user=params.dolphin_user)
    time.sleep(5)

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_process_status(status_params.dolphin_run_dir + "worker-server/pid")


if __name__ == "__main__":
  DolphinWorkerService().execute()
