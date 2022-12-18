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

import azkaban
from resource_management import *


class WebServer(Script):
    def install(self, env):
        import params
        env.set_params(params)
        install_cmd = "yum install -y azkaban_*-web"
        Execute(install_cmd)
        # exe script
        azkaban.executor_azkaban_sql()
        self.configure(env)
        Logger.info("install azkaban web success")

    def configure(self, env):
        import params
        env.set_params(params)
        azkaban.web_common_setup()

    def stop(self, env):
        import params
        Execute('{0}/bin/shutdown-web.sh'.format(params.azkaban_base_dir),
                user=params.azkaban_user)

    def start(self, env):
        import params
        self.configure(env)
        Execute('cd {0};./bin/start-web.sh'.format(params.azkaban_base_dir),
                user=params.azkaban_user)

    def status(self, env):
        try:
            import params
            self.configure(env)
            Execute(
                'export AZ_CNT=`ps -ef |grep -v grep |grep azkaban-web-server | wc -l` && `if [ $AZ_CNT -ne 0 ];then exit 0;else exit 3;fi `',
                user=params.azkaban_user
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef


if __name__ == '__main__':
    WebServer().execute()
