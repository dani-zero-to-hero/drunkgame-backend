"""
This api has the routes to handle matches
"""
from aiohttp import web

# from ..match import Match as DrunkMatch

routes = web.RouteTableDef()


@routes.get("/match")
async def get_matches(_: web.Request) -> web.Response:
    """
    Get a list of matches
    """
    return web.json_response()


# @routes.post("/match")
# async def create_match(request: web.Request) -> web.Response:
#     """
#     Create a new match
#     """
#     body = await request.json()
#     result = (await DrunkMatch.new_match(**body)).match_state
#     return web.json_response(data=result, status=200)


# @routes.get("/match/{match_id}")
# async def get_match_state(request: web.Request) -> web.Response:
#     """
#     Get current state of a match
#     """
#     match = await DrunkMatch.get_match(match_id=request.match_info["match_id"])
#     return web.json_response(data=match.match_state)


# @routes.delete("/match/{match_id}")
# async def delete_match(request: web.Request) -> web.Response:
#     """
#     Delete the given match from our DB
#     """
#     match = await DrunkMatch.get_match(match_id=request.match_info["match_id"])
#     return web.json_response(data=match.match_state)


# @routes.patch("/match/{match_id}")
# async def update_match(request: web.Request) -> web.Response:
#     """
#     Update a match with the request given, it can be user input, or others
#     """
#     match = await DrunkMatch.get_match(match_id=request.match_info["match_id"])
#     if match.update(await request.json()):
#         return web.json_response(data=match.match_state)
#     return web.json_response(text="Something went wrong", status=500)
