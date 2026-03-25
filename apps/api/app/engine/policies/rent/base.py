"""Shared interfaces and helpers for rent policies."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.engine.models import TitleDeed


class RentPolicy(Protocol):
    def calculate(
        self,
        deed: TitleDeed,
        *,
        dice_roll: int,
        owner_assets: list[TitleDeed],
    ) -> int: ...


def cannot_collect_rent(deed: TitleDeed) -> bool:
    return deed.owner_id is None or deed.is_mortgaged
