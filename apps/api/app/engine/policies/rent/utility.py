"""Rent policy for utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .base import cannot_collect_rent

if TYPE_CHECKING:
    from app.engine.models.title_deed import TitleDeed

TOTAL_UTILITIES = 2


@dataclass(frozen=True, slots=True)
class UtilityRentPolicy:
    """Rent strategy for utility spaces.

    Unlike properties and railroads, utility rent is *dice-dependent*:

    * **One utility owned** -- rent is ``4 x dice_roll``.
    * **Both utilities owned (monopoly)** -- rent is ``10 x dice_roll``.
    """

    def calculate(
        self,
        deed: TitleDeed,
        *,
        dice_roll: int,
        owner_assets: list[TitleDeed],
    ) -> int:
        """Return the rent owed for landing on a utility.

        Args:
            deed: The utility's title deed.
            dice_roll: Sum of the dice -- directly multiplied to
                determine the final rent.
            owner_assets: All title deeds owned by the utility's owner.

        Returns:
            Rent in dollars, or ``0`` if the deed is unowned, mortgaged,
            or not a ``Utility``.

        """
        if cannot_collect_rent(deed):
            return 0

        if deed.__class__.__name__ != "Utility":
            return 0

        utilities_owned = sum(
            1 for asset in owner_assets if asset.__class__.__name__ == "Utility"
        )
        if utilities_owned == 0:
            return 0

        has_monopoly = utilities_owned == TOTAL_UTILITIES
        multiplier = 10 if has_monopoly else 4

        return dice_roll * multiplier
