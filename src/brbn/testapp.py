from brbn import *
from brbn.plano import *

app = object()
server = Server(app)

class MainResource(Resource):
    async def render(self, request, entity):
        return "main"

temp_dir = make_temp_dir()

write(join(temp_dir, "alpha.txt"), "alpha")
write(join(temp_dir, "beta.html"), "beta")

server.add_route("/", MainResource(app))
server.add_route("/greek/*", FileResource(app, temp_dir))
