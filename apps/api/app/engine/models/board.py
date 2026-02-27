"""Board model for the Monopoly game engine."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .space import Space


@dataclass
class Board:
    """Represents the Monopoly game board."""

    spaces: list[Space] = field(default_factory=list)
    name: str = "Standard Monopoly"

    def get_space_at(self, position: int) -> Space:
        """Help get space, ensuring wrap around 40-slot board."""
        return self.spaces[position % len(self.spaces)]

    def find_space_by_id(self, space_id: str) -> Space | None:
        """Help find specific property by its string ID."""
        for space in self.spaces:
            if space.id == space_id:
                return space
        return None
