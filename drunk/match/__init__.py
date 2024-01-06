"""
Match module, this module handles all relations between game and players in matches. Also takes care of saving
information to databases
"""
import uuid
from typing import Any

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from ..games import Game
from ..players import Player

random_id_generators = [uuid.uuid1, uuid.uuid3, uuid.uuid4, uuid.uuid5]


class MatchState(BaseModel):
    """
    Pydantic class to create/update and more generally control the match status.

    :param started: Has the match started already or not. Note that ended matches can be started or not.
    :param paused: Is the match paused?? it could be that a match is waiting for players to join or the players want to
        continue another day
    :param ended: Has the match come to an end?
    """

    started: bool
    paused: bool
    ended: bool


class MatchResult(BaseModel):
    winners: list[Player]
    game: Game


class MatchTurnResult(BaseModel):
    ...


class Match(BaseModel):
    """
    A match is a relation between players and a game. This relation is unique but a set of players can play the same
    game and a game can be played by multiple sets of players.
    """

    match_id: str
    players: list[Player]
    match_type: str
    match_state: MatchState
    _match_result: MatchResult | None
    game: Game
    name: str
    _turns: list[MatchTurnResult]

    def _save_match(self) -> bool:
        return False

    def update(self, update: Any) -> bool:
        return bool(update)

    @property
    def has_ended(self) -> bool:
        """
        Has the match ended? is there a winner?? update and return the status
        """
        if self.game.end_reached and not self.match_state.ended:
            self.match_state.ended = self.game.end_reached
            self._match_result = MatchResult(winners=self.players, game=self.game)
            self._save_match()
        return self.match_state.ended

    @property
    def match_result(self) -> MatchResult | None:
        """
        Return the result of the current match. If the match has not ended None will be returned.
        """
        if self.has_ended:
            return None
        return self._match_result
