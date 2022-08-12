import brbn

app = object()
server = brbn.Server(app)

@server.route(path="/")
class MainResource(brbn.Resource):
    async def render(self, request, entity):
        return "Halloo"

if __name__ == "__main__":
    server.run()
