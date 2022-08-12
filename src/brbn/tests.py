#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from .plano import *
from threading import Thread

import asyncio
import httpx
import brbn
import brbn.testapp

class TestServer:
    async def __aenter__(self):
        port = get_random_port()

        self.task = asyncio.create_task(brbn.testapp.run_async("localhost", port))

        await brbn.testapp.server.started.wait()

        return f"http://localhost:{port}"

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.task.cancel()

        try:
            await self.task
        except asyncio.CancelledError:
            pass

@test
def anything_at_all():
    async def test():
        async with TestServer() as url:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

        print(response.text)

    asyncio.run(test())

def main():
    from .plano.commands import PlanoTestCommand
    import brbn.tests

    PlanoTestCommand(brbn.tests).main()
