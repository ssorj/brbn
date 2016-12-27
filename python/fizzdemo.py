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

from fizz import *

_strings = StringCatalog(__file__)

class Demo(Application):
    def __init__(self, home):
        super().__init__(home)

        self.root_resource = IndexPage(self)

class IndexPage(Page):
    def __init__(self, app):
        super().__init__(app, "/", _strings["index"])

        self.x = StringParameter(self, "x")

        self.form = Form(self, "form0")

        address_param = StringParameter(self, "address")

        address_input = FormInput(self.form, address_param)
        address_input.title = "Address"
        address_input.description = "The address of an AMQP node, such as a queue"

        submit_param = BooleanParameter(self, "submit")

        submit_button = FormButton(self.form, submit_param)
        submit_button.title = "Submit"

    def get_title(self, request):
        return "Fizz!"

    def process(self, request):
        self.form.process(request)

    @xml
    def render_x(self, request):
        return self.x.get(request)

    @xml
    def render_form(self, request):
        return self.form.render(request)
