"""Player model for the Monopoly game engine."""

from dataclasses import dataclass, field


@dataclass
class Player:
    """Represents a player in the Monopoly game."""

    id: str
    name: str
    position: int = 0
    cash: int = 1500
    property_ids: list[str] = field(default_factory=list)
    in_jail: bool = False
    jail_turns: int = 0
    is_bankrupt: bool = False
