"""Rent policy for properties."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .base import cannot_collect_rent

if TYPE_CHECKING:
    from app.engine.models.title_deed import TitleDeed


@dataclass(frozen=True, slots=True)
class PropertyRentPolicy:
    """Rent strategy for colour-group properties.

    Rent escalates through three tiers:

    1. **Houses / hotel** -- if the property has at least one house, the
       fixed amount from ``deed.house_rents`` is used.
    2. **Monopoly (no houses)** -- if the owner holds every property in
       the colour group, base rent is doubled.
    3. **Base** -- the unimproved rent printed on the deed.
    """

    def calculate(
        self,
        deed: TitleDeed,
        *,
        dice_roll: int,  # noqa: ARG002
        owner_assets: list[TitleDeed],
    ) -> int:
        """Return the rent owed for landing on a colour-group property.

        Args:
            deed: The property's title deed.
            dice_roll: Ignored -- property rent is not dice-dependent.
            owner_assets: All title deeds owned by the property's owner.

        Returns:
            Rent in dollars, or ``0`` if the deed is unowned, mortgaged,
            or not a ``Property``.

        """
        if cannot_collect_rent(deed):
            return 0

        if deed.__class__.__name__ != "Property":
            return 0

        if deed.num_houses > 0:
            return deed.house_rents[deed.num_houses - 1]

        same_color_owned = sum(
            1
            for asset in owner_assets
            if asset.__class__.__name__ == "Property" and asset.color == deed.color
        )

        has_monopoly = same_color_owned == deed.group_size

        return deed.base_rent * 2 if has_monopoly else deed.base_rent
