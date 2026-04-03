"""Response DTO exports."""

from .board import BoardDTO
from .error import ErrorDTO
from .game_state import GameStateDTO
from .player import PlayerDTO
from .spaces import PropertyDTO, RailroadDTO, SpaceDTO, SpecialSpaceDTO, UtilityDTO

__all__ = [
    "BoardDTO",
    "ErrorDTO",
    "GameStateDTO",
    "PlayerDTO",
    "PropertyDTO",
    "RailroadDTO",
    "SpaceDTO",
    "SpecialSpaceDTO",
    "UtilityDTO",
]
