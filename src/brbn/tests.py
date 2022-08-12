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

# test_cert_dir = join(get_parent_dir(__file__), "testcerts")

# class TestServer:
#     def __init__(self, **extra_args):
#         port = get_random_port()
#         args = " ".join(["--{} {}".format(k, v) for k, v in extra_args.items()])

#         self.proc = start(f"qbroker --verbose --port {port} {args}")
#         self.proc.url = f"//localhost:{port}/queue1"

#     def __enter__(self):
#         return self.proc

#     def __exit__(self, exc_type, exc_value, traceback):
#         stop(self.proc)

# @test(timeout=5)
# def version():
#     result = call("brbn --version")

# @test(timeout=5)
# def logging():
#     result = call("brbn --version")
#     assert result

#     run("brbn --init-only --quiet")
#     run("brbn --init-only --verbose")

@test
def hello():
    print("Hi")

def main():
    from .plano.commands import PlanoTestCommand
    import brbn.tests

    PlanoTestCommand(brbn.tests).main()
