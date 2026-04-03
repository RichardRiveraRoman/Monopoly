"""Request DTOs for mortgage actions."""

from app.schemas.common import ApiSchema, PlayerId, SpaceId


class MortgagePropertyRequest(ApiSchema):
    """Payload for mortgaging an owned property."""

    player_id: PlayerId
    space_id: SpaceId
