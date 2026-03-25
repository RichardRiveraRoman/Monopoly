"""Standard color-group property model."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.engine.policies.rent import PropertyRentPolicy

from .title_deed import TitleDeed

if TYPE_CHECKING:
    from app.engine.policies.rent.base import RentPolicy


@dataclass(slots=True)
class Property(TitleDeed):
    """Standard color-group property (Ex: Boardwalk)."""

    base_rent: int = 0
    house_rents: list[int] = field(default_factory=list)
    num_houses: int = 0
    house_cost: int = 0
    group_size: int = 0
    rent_policy: RentPolicy = field(
        default_factory=PropertyRentPolicy,
        repr=False,
        compare=False,
    )

    def calculate_rent(self, dice_roll: int, owner_assets: list[TitleDeed]) -> int:
        """Return rent owed for this property."""
        return self.rent_policy.calculate(
            self,
            dice_roll=dice_roll,
            owner_assets=owner_assets,
        )
