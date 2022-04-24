from aiohttp import web

routes = web.RouteTableDef()


@routes.view("/match")
class Match(web.View):
    async def post(self):
        pass

    async def get(self):
        pass


@routes.view("/match/{match_id}")
class SingleMatch(web.View):
    async def put(self):
        pass

    async def get(self):
        pass

    async def delete(self):
        pass

    async def patch(self):
        pass
