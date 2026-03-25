"""Rent policy for properties."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.engine.models import Property

from .base import cannot_collect_rent

if TYPE_CHECKING:
    from app.engine.models import TitleDeed


@dataclass(frozen=True, slots=True)
class PropertyRentPolicy:
    def calculate(
        self,
        deed: TitleDeed,
        *,
        dice_roll: int,  # noqa: ARG002
        owner_assets: list[TitleDeed],
    ) -> int:

        if cannot_collect_rent(deed):
            return 0

        if not isinstance(deed, Property):
            return 0

        if deed.num_houses > 0:
            return deed.house_rents[deed.num_houses - 1]

        same_color_owned = sum(
            1
            for asset in owner_assets
            if isinstance(asset, Property) and asset.color == deed.color
        )

        has_monopoly = same_color_owned == deed.group_size

        return deed.base_rent * 2 if has_monopoly else deed.base_rent
