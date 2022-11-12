from aiohttp import web

routes = web.RouteTableDef()


@routes.view("/match")
class Match(web.View):
    async def post(self):
        # Create a new match
        pass

    async def get(self):
        # Get a list of matches
        pass


@routes.view("/match/{match_id}")
class SingleMatch(web.View):
    async def put(self):
        pass

    async def get(self):
        # Get current state of a match
        pass

    async def delete(self):
        pass

    async def patch(self):
        pass
