"""Utility property model."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.engine.policies.rent import UtilityRentPolicy

from .title_deed import TitleDeed

if TYPE_CHECKING:
    from app.engine.policies.rent.base import RentPolicy


@dataclass(slots=True)
class Utility(TitleDeed):
    """Utilities (Electric/Water - rent depends on dice roll)."""

    rent_policy: RentPolicy = field(
        default_factory=UtilityRentPolicy,
        repr=False,
        compare=False,
    )

    def calculate_rent(self, dice_roll: int, owner_assets: list[TitleDeed]) -> int:
        """Return rent as a dice-roll multiplier based on utilities owned."""
        return self.rent_policy.calculate(
            self,
            dice_roll=dice_roll,
            owner_assets=owner_assets,
        )
