"""Aggregate root for a Monopoly game session."""

from __future__ import annotations

from dataclasses import dataclass

from .board import Board
from .board_skeleton import get_board_spaces
from .player import Player

MIN_PLAYERS = 2
MAX_PLAYERS = 8


@dataclass(slots=True)
class GameState:
    """Mutable aggregate root for a single Monopoly game."""

    game_id: str
    players: list[Player]
    board: Board

    @classmethod
    def create(cls, *, game_id: str, player_names: list[str]) -> GameState:
        """Create a new game using the standard Monopoly board."""
        players = [
            Player(id=f"player_{index}", name=name)
            for index, name in enumerate(player_names, start=1)
        ]
        board = Board(spaces=get_board_spaces())

        return cls(game_id=game_id, players=players, board=board)
