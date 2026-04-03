"""Request DTOs for creating a new game."""

from pydantic import Field

from app.schemas.common import ApiSchema, PlayerName


class CreateGameRequest(ApiSchema):
    """Payload for creating a new Monopoly game."""

    player_names: list[PlayerName] = Field(min_length=2, max_length=8)
