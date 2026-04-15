"""Shared interfaces and helpers for rent policies."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.engine.models.title_deed import TitleDeed


class RentPolicy(Protocol):
    """Structural interface that all rent-calculation strategies must satisfy.

    Concrete implementations (e.g. ``PropertyRentPolicy``,
    ``RailroadRentPolicy``, ``UtilityRentPolicy``) are free to use any
    internal logic they need as long as they expose a ``calculate`` method
    with this exact signature.
    """

    def calculate(
        self,
        deed: TitleDeed,
        *,
        dice_roll: int,
        owner_assets: list[TitleDeed],
    ) -> int:
        """Return the rent amount owed for landing on *deed*.

        Args:
            deed: The title deed of the space a player has landed on.
            dice_roll: Sum of the dice that triggered the landing. Only
                relevant for utility rent; other policies may ignore it.
            owner_assets: Every title deed currently held by the deed's
                owner, used to determine monopoly / group bonuses.

        Returns:
            The rent in dollars. ``0`` when rent cannot be collected
            (e.g. unowned or mortgaged deed).

        """
        ...


def cannot_collect_rent(deed: TitleDeed) -> bool:
    """Return ``True`` if the deed is unowned or mortgaged."""
    return deed.owner_id is None or deed.is_mortgaged
