"""Utility property model."""

from dataclasses import dataclass

from .title_deed import TitleDeed

TOTAL_UTILITIES = 2


@dataclass
class Utility(TitleDeed):
    """Utilities (Electric/Water - rent depends on dice roll)."""

    def calculate_rent(self, dice_roll: int, owner_assets: list[TitleDeed]) -> int:
        """Return rent as a dice-roll multiplier based on utilities owned."""
        if self.owner_id is None or self.is_mortgaged:
            return 0

        utilities_owned = sum(1 for p in owner_assets if isinstance(p, Utility))

        if utilities_owned == 0:
            return 0

        has_monopoly = utilities_owned == TOTAL_UTILITIES
        multiplier = 10 if has_monopoly else 4
        return dice_roll * multiplier
