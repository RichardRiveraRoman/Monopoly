"""Response DTOs for the game board."""

from app.schemas.common import ApiSchema


class BoardDTO(ApiSchema):
    """Serialized view of a Monopoly board."""

    name: str
    spaces: list[SpaceDTO]
