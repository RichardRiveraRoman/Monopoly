"""Response DTO for the board spaces."""

from typing import TYPE_CHECKING, Annotated, Literal

from pydantic import Field

from app.engine.models import SpaceType
from app.schemas.common import ApiSchema, PlayerId, SpaceId

if TYPE_CHECKING:
    from app.engine.models import SpaceColor


class BaseSpaceDTO(ApiSchema):
    """Fields shared by every board-sace representation."""

    id: SpaceId
    name: str
    color: SpaceColor


class OwnableSpaceDTO(BaseSpaceDTO):
    """Fields share by ownable title-deed spaces."""

    owner_id: PlayerId | None = None
    purchase_price: int
    base_rent: int
    is_mortgaged: bool


class PropertyDTO(OwnableSpaceDTO):
    """Serialized view of standard colour-group property."""

    type: Literal[SpaceType.PROPERTY] = SpaceType.PROPERTY
    base_rent: int
    house_rents: list[int]
    num_houses: int
    house_cost: int
    group_size: int


class RailroadDTO(OwnableSpaceDTO):
    """Serialized view of a railroad space."""

    type: Literal[SpaceType.STATION] = SpaceType.STATION
    rent_levels: list[int]


class UtilityDTO(OwnableSpaceDTO):
    """Serialized view of a utility space."""

    type: Literal[SpaceType.UTILITY] = SpaceType.UTILITY


class SpecialSpaceDTO(BaseSpaceDTO):
    """Serialized view of non-ownable board spaces."""

    type: Literal[SpaceType.SPECIAL] = SpaceType.SPECIAL


SpaceDTO = Annotated[
    PropertyDTO | RailroadDTO | UtilityDTO | SpecialSpaceDTO,
    Field(discriminator="type"),
]
