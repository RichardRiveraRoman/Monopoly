"""Unit tests for purchase rule helpers."""

from app.engine.models.player import Player
from app.engine.models.property import Property
from app.engine.models.space import SpaceColor, SpaceType
from app.engine.rules.purchases import (
    buy_property,
    decline_property,
    resolve_unowned_landing,
)


def _make_deed(*, deed_id: str = "med_ave", price: int = 60) -> Property:
    return Property(
        id=deed_id,
        name="Mediterranean Avenue",
        color=SpaceColor.BROWN,
        type=SpaceType.PROPERTY,
        purchase_price=price,
        base_rent=2,
        mortgage_value=30,
    )


def test_resolve_unowned_landing_returns_buy_or_auction_payload() -> None:
    """Landing on unowned deed should return buy-or-auction decision event."""
    player = Player(id="p1", name="Alice")
    deed = _make_deed(deed_id="reading_rr", price=200)

    result = resolve_unowned_landing(player, deed)

    assert result == {
        "type": "buy_or_auction",
        "player_id": "p1",
        "space_id": "reading_rr",
        "price": 200,
    }


def test_buy_property_returns_insufficient_funds_payload() -> None:
    """Buying should fail with insufficient_funds when player cannot afford deed."""
    player = Player(id="p1", name="Alice", cash=50)
    deed = _make_deed(price=60)

    result = buy_property(player, deed)

    assert result == {
        "type": "insufficient_funds",
        "player_id": "p1",
        "space_id": "med_ave",
        "required": 60,
        "cash": 50,
    }
    assert player.cash == 50
    assert deed.owner_id is None
    assert player.property_ids == []


def test_buy_property_purchases_and_mutates_state() -> None:
    """Buying should deduct cash, assign deed owner, and append property id."""
    player = Player(id="p1", name="Alice", cash=200)
    deed = _make_deed(price=60)

    result = buy_property(player, deed)

    assert result == {
        "type": "property_bought",
        "player_id": "p1",
        "space_id": "med_ave",
        "price": 60,
    }
    assert player.cash == 140
    assert deed.owner_id == "p1"
    assert player.property_ids == ["med_ave"]


def test_decline_property_returns_start_auction_payload() -> None:
    """Declining purchase should emit start_auction payload."""
    player = Player(id="p1", name="Alice")
    deed = _make_deed(deed_id="water_works", price=150)

    result = decline_property(player, deed)

    assert result == {
        "type": "start_auction",
        "player_id": "p1",
        "space_id": "water_works",
        "starting_price": 1,
    }
