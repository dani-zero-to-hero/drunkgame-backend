import uuid

from pydantic import BaseModel

from ..games import Game
from ..players import Player

random_id_generators = [uuid.uuid1, uuid.uuid3, uuid.uuid4, uuid.uuid5]


class MatchState(BaseModel):
    started: bool
    paused: bool
    ended: bool


class MatchResult(BaseModel):
    winners: list[Player]
    game: Game


class MatchTurnResult(BaseModel):
    ...


class Match(BaseModel):
    match_id: str
    players: list[str]
    match_type: str
    match_state: MatchState
    _match_result: MatchResult | None
    game: Game
    name: str
    _turns: list[MatchTurnResult]

    @classmethod
    async def new_match(cls) -> "Match":
        match = cls()
        match._save_match()
        return match

    @classmethod
    async def get_match(cls, match_id: str) -> "Match":
        return cls()

    def _save_match(self) -> bool:
        pass

    def update(self, update) -> bool:
        pass

    @property
    def has_ended(self) -> bool:
        if self.game.end_reached and not self.match_state.ended:
            self.match_state.ended = self.game.end_reached
            self._match_result = MatchResult(winners=self.players, game=self.game)
            self._save_match()
        return self.match_state.ended

    @property
    def match_result(self) -> MatchResult | None:
        if self.has_ended:
            return None
        return self._match_result
