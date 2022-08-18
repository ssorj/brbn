from brbn import *
from brbn.plano import *

temp_dir = make_temp_dir()

write(join(temp_dir, "alpha.txt"), "alpha")
write(join(temp_dir, "beta.html"), "beta")

server = Server()

class Main(Resource):
    async def render(self, request, entity):
        return "main"

class Explode(Resource):
    async def process(self, request):
        raise Exception()

class Files(FileResource):
    def __init__(self):
        super().__init__(dir=temp_dir)

class Json(Resource):
    async def process(self, request):
        data = await request.parse_json()

class PostOnly(Resource):
    def __init__(self):
        super().__init__(methods=("POST",))

class RequiredParam(Resource):
    async def process(self, request):
        request.require("not-there")

server.add_route("/", Main())
server.add_route("/explode", Explode())
server.add_route("/files/*", Files())
server.add_route("/json", Json())
server.add_route("/post-only", PostOnly())
server.add_route("/required-param", RequiredParam())
