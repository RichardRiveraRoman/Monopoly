"""Rent policy for railroads."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.engine.models import Railroad

from .base import cannot_collect_rent

if TYPE_CHECKING:
    from app.engine.models import TitleDeed

TOTAL_RAILROADS = 4


@dataclass(frozen=True, slots=True)
class RailroadRentPolicy:
    def calculate(
        self,
        deed: TitleDeed,
        *,
        dice_roll: int,  # noqa: ARG002
        owner_assets: list[TitleDeed],
    ) -> int:
        if cannot_collect_rent(deed):
            return 0

        if not isinstance(deed, Railroad):
            return 0

        railroads_owned = sum(
            1 for asset in owner_assets if isinstance(asset, Railroad)
        )

        rent_level = min(
            railroads_owned,
            TOTAL_RAILROADS,
            len(deed.rent_levels),
        )

        if rent_level == 0:
            return 0

        return deed.rent_levels[rent_level - 1]
