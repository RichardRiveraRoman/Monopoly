"""Rent policy for utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.engine.models import Utility

from .base import cannot_collect_rent

if TYPE_CHECKING:
    from app.engine.models import TitleDeed

TOTAL_UTILITIES = 2


@dataclass(frozen=True, slots=True)
class UtilityRentPolicy:
    def calculate(
        self,
        deed: TitleDeed,
        *,
        dice_roll: int,
        owner_assets: list[TitleDeed],
    ) -> int:
        if cannot_collect_rent(deed):
            return 0

        if not isinstance(deed, Utility):
            return 0

        utilities_owned = sum(1 for asset in owner_assets if isinstance(asset, Utility))
        if utilities_owned == 0:
            return 0

        has_monopoly = utilities_owned == TOTAL_UTILITIES
        multiplier = 10 if has_monopoly else 4

        return dice_roll * multiplier
