"""Railroad property model."""

from dataclasses import dataclass, field

from .title_deed import TitleDeed

TOTAL_RAILROADS = 4


@dataclass
class Railroad(TitleDeed):
    """Railroad/Stations (rent depends on how many railroads the owner has)."""

    rent_levels: list[int] = field(default_factory=lambda: [25, 50, 100, 200])

    def calculate_rent(self, dice_roll: int, owner_assets: list[TitleDeed]) -> int:  # noqa: ARG002
        """Return rent based on how many railroads the owner holds."""
        if self.owner_id is None or self.is_mortgaged:
            return 0

        railroads_owned = sum(1 for p in owner_assets if isinstance(p, Railroad))

        if railroads_owned == 0:
            return 0

        return self.rent_levels[railroads_owned - 1]
