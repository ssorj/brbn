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

import logging as _logging

from brbn import *
from pencil import *

_log = _logging.getLogger("fizz")

class Parameter:
    def __init__(self, resource, name):
        self._resource = resource
        self._name = name

        self.required = True
        self.default_value = None

    @property
    def resource(self):
        return self._resource

    @property
    def name(self):
        return self._name

    def unmarshal(self, request, strings):
        raise NotImplementedError()

    def marshal(self, request, object_):
        raise NotImplementedError()
    
    def get(self, request):
        strings = request.parameters.get(self.name)

        if strings is None:
            return self.get_default_value(request)

        return self.unmarshal(request, strings)
        
    def get_default_value(self, request):
        return self.default_value

class StringParameter(Parameter):
    """
    A parameter for strings

    :var max_length: The maximum allowed string length (default 256)
    :vartype max_length: int
    """

    def __init__(self, resource, name):
        super(StringParameter, self).__init__(resource, name)

        self.max_length = 256

    def unmarshal(self, request, strings):
        return strings[0]

    def marshal(self, request, object_):
        return [object_]

    def do_validate(self, request, object_):
        if len(object_) > self.max_length:
            self.add_error(request, "String exceeds maximum length")

class SymbolParameter(StringParameter):
    """
    A restricted string parameter allowing only symbol characters
    Allowed characters are numbers, letters, and underscore.
    """

    def do_validate(self, request, object_):
        string = object_.replace("_", "")

        if not string.isalnum():
            self.add_error(request, "Symbol has illegal characters")

class SecretParameter(StringParameter):
    """
    A string parameter whose debug output is hidden
    """

    pass

class IntegerParameter(Parameter):
    """
    A parameter for integers
    """

    def unmarshal(self, request, strings):
        return int(strings[0])

    def marshal(self, request, object_):
        return [str(object_)]

class FloatParameter(Parameter):
    """
    A parameter for floats
    """

    def unmarshal(self, request, strings):
        return float(strings[0])

    def marshal(self, request, object_):
        return [str(object_)]

class BooleanParameter(Parameter):
    """
    A parameter for `True` and `False`
    """

    def unmarshal(self, request, strings):
        return strings[0] == "t"

    def marshal(self, request, object_):
        if object_ is True:
            return ["t"]
        else:
            return ["f"]

_form_template = """
<form method="get" action="?" class="fizz-form">
  {inputs}

  {submit_button} {cancel_button}
</form>
"""

_form_input_template = """
<div class="fizz-input">
  <h2>{title}</h2>

  {description}
  {input_element}
</div>
"""

_form_button_template = """
<button class="fizz-button" name="{parameter_name}" value="{parameter_value}">{title}</button>
"""

class Form:
    def __init__(self, resource, name):
        self._resource = resource
        self._name = name

        self.inputs = list()

        self._state_param = SymbolParameter(self.resource, "{}_state".format(self.name))

        self._submit_button = SubmitButton(self, self._state_param)
        self._cancel_button = CancelButton(self, self._state_param)
        
        self._template = Template(_form_template, self)
        
    @property
    def resource(self):
        return self._resource

    @property
    def name(self):
        return self._name

    def process(self, request):
        if self._state_param.get(request) == "submit":
            print("Processing form")
    
    @xml
    def render(self, request):
        return self._template.render(request)
    
    @xml
    def render_inputs(self, request):
        out = list()
        
        for input in self.inputs:
            out.append(input.render(request))

        return "".join(out)

    @xml
    def render_submit_button(self, request):
        return self._submit_button.render(request)

    @xml
    def render_cancel_button(self, request):
        return self._cancel_button.render(request)

class _FormComponent:
    def __init__(self, form, parameter, template):
        self._form = form
        self._parameter = parameter

        self.title = None
        self.description = None

        self._template = Template(template, self)

    @property
    def form(self):
        return self._form
        
    @property
    def parameter(self):
        return self._parameter

    @xml
    def render(self, request):
        return self._template.render(request)
    
    def render_title(self, request):
        return self.title

    def render_description(self, request):
        return self.description

class FormInput(_FormComponent):
    def __init__(self, form, parameter):
        super().__init__(form, parameter, _form_input_template)

        self.form.inputs.append(self)

    @xml
    def render_input_element(self, request):
        return html_input("", name=self.parameter.name)

class FormButton(_FormComponent):
    def __init__(self, form, parameter):
        super().__init__(form, parameter, _form_button_template)

    def render_parameter_name(self, request):
        return self.parameter.name

class SubmitButton(FormButton):
    def __init__(self, form, parameter):
        super().__init__(form, parameter)

    def render_title(self, request):
        return "Submit"

    def render_parameter_value(self, request):
        return "submit"

class CancelButton(FormButton):
    def __init__(self, form, parameter):
        super().__init__(form, parameter)

    def render_title(self, request):
        return "Cancel"

    def render_parameter_value(self, request):
        return "cancel"
