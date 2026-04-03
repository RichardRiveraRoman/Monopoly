"""Common schema helpers shared across request and response DTOs."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

GameId = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
PlayerId = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
PlayerName = Annotated[
    str,
    StringConstraints(min_length=1, max_length=12, strip_whitespace=True),
]
SpaceId = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]


class ApiSchema(BaseModel):
    """Base class for API boundary DTOs."""

    model_config = ConfigDict(extra="forbid")
