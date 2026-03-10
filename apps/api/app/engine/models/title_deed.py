"""Title deed model for ownable board spaces."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass

from .space import Space


@dataclass
class TitleDeed(Space):
    """A Space that can be owned, bought, and rented."""

    owner_id: str | None = None
    purchase_price: int = 0
    base_rent: int = 0
    mortgage_value: int = 0
    is_mortgaged: bool = False

    @abstractmethod
    def calculate_rent(self, dice_roll: int, owner_assets: list[TitleDeed]) -> int:
        """To be overridden by specific property types."""
