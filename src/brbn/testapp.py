from brbn import *
from brbn.plano import *

static_dir = make_temp_dir()

write(join(static_dir, "alpha.txt"), "alpha")
write(join(static_dir, "beta.html"), "beta")

server = Server()

class Main(Resource):
    async def render(self, request, entity):
        return "main"

class Explode(Resource):
    async def process(self, request):
        raise Exception()

class Json(Resource):
    async def process(self, request):
        data = await request.parse_json()

class PostOnly(Resource):
    def __init__(self):
        super().__init__(method="POST")

class RequiredParam(Resource):
    async def process(self, request):
        request.require("not-there")

server.add_route("/", Main())
server.add_route("/explode", Explode())
server.add_route("/files/alpha.txt", PinnedFileResource(join(static_dir, "alpha.txt")))
server.add_route("/files/*", StaticDirectoryResource(static_dir))
server.add_route("/json", Json())
server.add_route("/post-only", PostOnly())
server.add_route("/required-param", RequiredParam())
