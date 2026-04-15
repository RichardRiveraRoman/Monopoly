"""Purchase decision rules for ownable spaces."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.engine.models import Player, TitleDeed


def resolve_unowned_landing(player: Player, deed: TitleDeed) -> dict:
    """Return event prompting buy-or-auction for an unowned deed."""
    return {
        "type": "buy_or_auction",
        "player_id": player.id,
        "space_id": deed.id,
        "price": deed.purchase_price,
    }


def buy_property(player: Player, deed: TitleDeed) -> dict:
    """Attempt to buy an unowned deed and return outcome payload."""
    if player.cash < deed.purchase_price:
        return {
            "type": "insufficient_funds",
            "player_id": player.id,
            "space_id": deed.id,
            "required": deed.purchase_price,
            "cash": player.cash,
        }

    player.cash -= deed.purchase_price
    player.property_ids.append(deed.id)
    deed.owner_id = player.id
    return {
        "type": "property_bought",
        "player_id": player.id,
        "space_id": deed.id,
        "price": deed.purchase_price,
    }


def decline_property(player: Player, deed: TitleDeed) -> dict:
    """Return event to start auction when player declines purchase."""
    return {
        "type": "start_auction",
        "player_id": player.id,
        "space_id": deed.id,
        "starting_price": 1,
    }
