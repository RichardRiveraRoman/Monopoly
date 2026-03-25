"""Railroad property model."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.engine.policies.rent import RailroadRentPolicy

from .title_deed import TitleDeed

if TYPE_CHECKING:
    from app.engine.policies.rent.base import RentPolicy


@dataclass(slots=True)
class Railroad(TitleDeed):
    """Railroad/Stations (rent depends on how many railroads the owner has)."""

    rent_levels: list[int] = field(default_factory=lambda: [25, 50, 100, 200])
    rent_policy: RentPolicy = field(
        default_factory=RailroadRentPolicy,
        repr=False,
        compare=False,
    )

    def calculate_rent(self, dice_roll: int, owner_assets: list[TitleDeed]) -> int:
        """Return rent based on how many railroads the owner holds."""
        return self.rent_policy.calculate(
            self,
            dice_roll=dice_roll,
            owner_assets=owner_assets,
        )
