"""Unit tests for ownership service functions."""

from app.engine.models.board import Board
from app.engine.models.board_skeleton import get_board_spaces
from app.engine.models.player import Player
from app.engine.services.ownership import (
    collect_owner_assets,
    find_owner,
    transfer_rent,
)


def test_find_owner_returns_matching_player() -> None:
    """Return the owner when a player has the requested property id."""
    players = [
        Player(id="p1", name="Alice", property_ids=[]),
        Player(id="p2", name="Bob", property_ids=["reading_rr"]),
    ]

    owner = find_owner(players, "reading_rr")

    assert owner is not None
    assert owner.id == "p2"


def test_find_owner_returns_none_when_unowned() -> None:
    """Return None when no player owns the requested space id."""
    players = [
        Player(id="p1", name="Alice", property_ids=[]),
        Player(id="p2", name="Bob", property_ids=[]),
    ]

    owner = find_owner(players, "reading_rr")

    assert owner is None


def test_collect_owner_assets_returns_only_title_deeds() -> None:
    """Collect only valid title deed spaces for listed owner properties."""
    board = Board(spaces=get_board_spaces())
    owner = Player(
        id="p1",
        name="Alice",
        property_ids=["reading_rr", "go", "unknown_space"],
    )

    assets = collect_owner_assets(board, owner)

    assert [asset.id for asset in assets] == ["reading_rr"]


def test_transfer_rent_returns_no_rent_due_for_non_positive_rent() -> None:
    """No transfer occurs when rent is zero or negative."""
    payer = Player(id="p1", name="Alice", cash=500)
    owner = Player(id="p2", name="Bob", cash=300)

    result = transfer_rent(payer, owner, 0)

    assert result == {
        "type": "no_rent_due",
        "payer_id": "p1",
        "owner_id": "p2",
        "rent": 0,
    }
    assert payer.cash == 500
    assert owner.cash == 300


def test_transfer_rent_pays_full_amount_when_payer_can_afford() -> None:
    """Rent is fully transferred and both balances update correctly."""
    payer = Player(id="p1", name="Alice", cash=500)
    owner = Player(id="p2", name="Bob", cash=300)

    result = transfer_rent(payer, owner, 200)

    assert result == {
        "type": "rent_paid",
        "payer_id": "p1",
        "owner_id": "p2",
        "rent": 200,
    }
    assert payer.cash == 300
    assert owner.cash == 500


def test_transfer_rent_marks_bankrupt_when_payer_cannot_afford() -> None:
    """When payer cannot cover rent, all cash is transferred and payer bankrupts."""
    payer = Player(id="p1", name="Alice", cash=120)
    owner = Player(id="p2", name="Bob", cash=300)

    result = transfer_rent(payer, owner, 200)

    assert result == {
        "type": "player_bankrupt",
        "payer_id": "p1",
        "owner_id": "p2",
        "rent_due": 200,
        "paid": 120,
        "shortfall": 80,
    }
    assert payer.cash == 0
    assert payer.is_bankrupt is True
    assert owner.cash == 420
