from typing import Any, Optional

from pydantic import BaseModel

from .games import Game


async def create_match(
    match_name: str, player_list: list[str], match_id: Optional[str] = None
):
    pass


class MatchState(BaseModel):
    started: bool


class Match(BaseModel):
    match_id: str
    players: list[str]
    match_type: str
    match_state: MatchState
    game: Game

    def __init__(__pydantic_self__, **data: Any) -> None:
        data["game"] = Game.get_game(data.get("game_type", ""))

        super().__init__(**data)

    def save_match(self) -> bool:
        pass

    def update(self, update) -> bool:
        pass

    def has_ended(self) -> bool:
        return self.game.end_reached
