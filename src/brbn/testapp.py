import brbn

app = object()
server = brbn.Server(app)

@server.route(path="/")
class MainResource(brbn.Resource):
    async def render(self, request, entity):
        return "Halloo"

async def run_async(host, port):
    await server.run_async(host=host, port=port)
