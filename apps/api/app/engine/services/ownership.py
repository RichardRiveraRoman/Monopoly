"""Ownership domain service functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.engine.models.title_deed import TitleDeed

if TYPE_CHECKING:
    from app.engine.models.board import Board
    from app.engine.models.player import Player


def find_owner(players: list[Player], space_id: str) -> Player | None:
    """Return the player who owns a given space, if any."""
    for player in players:
        if space_id in player.property_ids:
            return player
    return None


def collect_owner_assets(board: Board, owner: Player) -> list[TitleDeed]:
    """Return all ownable deeds currently held by the owner."""
    assets: list[TitleDeed] = []
    for property_id in owner.property_ids:
        space = board.find_space_by_id(property_id)
        if isinstance(space, TitleDeed):
            assets.append(space)
    return assets


def transfer_rent(payer: Player, owner: Player, rent: int) -> dict:
    """Transfer rent from payer to owner and return outcome event payload."""
    if rent <= 0:
        return {
            "type": "no_rent_due",
            "payer_id": payer.id,
            "owner_id": owner.id,
            "rent": 0,
        }

    if payer.cash >= rent:
        payer.cash -= rent
        owner.cash += rent
        return {
            "type": "rent_paid",
            "payer_id": payer.id,
            "owner_id": owner.id,
            "rent": rent,
        }

    paid = payer.cash
    owner.cash += paid
    payer.cash = 0
    payer.is_bankrupt = True
    return {
        "type": "player_bankrupt",
        "payer_id": payer.id,
        "owner_id": owner.id,
        "rent_due": rent,
        "paid": paid,
        "shortfall": rent - paid,
    }
