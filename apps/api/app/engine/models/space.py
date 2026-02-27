"""Space model for the Monopoly game engine."""

from dataclasses import dataclass
from enum import StrEnum


class SpaceColor(StrEnum):
    """Color groups for property spaces on the Monopoly board."""

    BROWN = "Brown"
    LIGHT_BLUE = "Light Blue"
    PINK = "Pink"
    ORANGE = "Orange"
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    DARK_BLUE = "Dark Blue"
    NONE = "None"  # For GO, Jail, etc.


class SpaceType(StrEnum):
    """Types of spaces on the Monopoly board."""

    PROPERTY = "Property"
    STATION = "Station"
    UTILITY = "Utility"
    SPECIAL = "Special"  # GO, Tax, Income Tax


@dataclass
class Space:
    """Represents a space in the Monopoly game."""

    id: str
    name: str
    color: SpaceColor
    type: SpaceType
