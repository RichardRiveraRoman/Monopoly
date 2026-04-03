"""Request DTOs for turn-ending actions."""

from app.schemas.common import ApiSchema, PlayerId


class EndTurnRequest(ApiSchema):
    """Payload for ending the current player's turn."""

    player_id: PlayerId
