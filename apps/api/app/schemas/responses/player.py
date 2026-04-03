"""Response DTOs for players."""

from app.schemas.common import ApiSchema, PlayerId, SpaceId


class PlayerDTO(ApiSchema):
    """Serialized view of a Monopoly player."""

    id: PlayerId
    name: str
    position: int
    cash: int
    property_ids: list[SpaceId]
    in_jail: bool
    jail_turns: int
    is_bankrupt: bool
