"""Request DTOs for dice-roll actions."""

from app.schemas.common import ApiSchema, PlayerId


class RollDiceRequest(ApiSchema):
    """Payload for rolling dice on a player's turn."""

    player_id: PlayerId
