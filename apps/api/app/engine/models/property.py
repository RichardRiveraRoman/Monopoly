"""Standard color-group property model."""

from dataclasses import dataclass, field

from .title_deed import TitleDeed


@dataclass
class Property(TitleDeed):
    """Standard color-group property (Ex: Boardwalk)."""

    base_rent: int = 0
    house_rents: list[int] = field(default_factory=list)
    num_houses: int = 0
    house_cost: int = 0

    def calculate_rent(self, dice_roll: int, owner_assets: list[TitleDeed]) -> int:  # noqa: ARG002
        """Return rent owed; doubles base rent when the owner holds a monopoly."""
        if self.is_mortgaged:
            return 0
        if self.num_houses > 0:
            return self.house_rents[self.num_houses - 1]

        has_monopoly = all(
            p.owner_id == self.owner_id
            for p in owner_assets
            if isinstance(p, Property) and p.color == self.color
        )

        return self.base_rent * 2 if has_monopoly else self.base_rent
