"""Request DTOs for property-purchase actions."""

from app.schemas.common import ApiSchema, PlayerId, SpaceId


class BuyPropertyRequest(ApiSchema):
    """Payload for purchasing an unowned property."""

    player_id: PlayerId
    space_id: SpaceId
