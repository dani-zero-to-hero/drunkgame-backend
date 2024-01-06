"""
Common endpoints for a server running the drunk game, like keep alive, api docs etc
"""
from aiohttp import web


async def keep_alive(_: web.Request) -> web.Response:
    return web.Response(text="I'm alive and well")


app = web.Application()
app.add_routes(
    [
        web.get("/keep-alive", keep_alive),
    ]
)

if __name__ == "__main__":
    web.run_app(app)
