"""Reponse DTOs for the game-state aggregate."""

from typing import TYPE_CHECKING

from app.schemas.common import ApiSchema, GameId, PlayerId

if TYPE_CHECKING:
    from app.engine.models import GamePhase
    from app.schemas.responses import BoardDTO, PlayerDTO


class GameStateDTO(ApiSchema):
    """Serialized view of a Monopoly game state."""

    id: GameId
    board: BoardDTO
    players: list[PlayerDTO]
    current_player_id: PlayerId | None = None
    current_player_index: int
    game_phase: GamePhase
    last_dice_roll: int
    end_game: bool
