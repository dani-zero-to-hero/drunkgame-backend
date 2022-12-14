from aiohttp import web

from . import Match as DrunkMatch

routes = web.RouteTableDef()


@routes.view("/match")
class Match(web.View):
    async def post(self, payload):
        # Create a new match
        return DrunkMatch(**payload).match_state

    async def get(self):
        # Get a list of matches
        pass


@routes.view("/match/{match_id}")
class SingleMatch(web.View):
    async def get(self, match_id):
        # Get current state of a match
        match = await DrunkMatch.get_match(match_id=match_id)
        return match.match_state

    async def delete(self):
        pass

    async def patch(self):
        pass
