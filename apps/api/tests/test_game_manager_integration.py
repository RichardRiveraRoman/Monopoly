"""Integration tests for GameManager compatibility behavior."""

import pytest

from app.engine.models.board import Board
from app.engine.models.board_skeleton import get_board_spaces
from app.engine.models.game_manager import GameManager
from app.engine.models.player import Player
from app.engine.models.title_deed import TitleDeed


def _make_manager_with_two_players() -> GameManager:
    board = Board(spaces=get_board_spaces())
    players = [
        Player(id="p1", name="Alice"),
        Player(id="p2", name="Bob"),
    ]
    return GameManager(board=board, players=players)


def _get_ownable_space(manager: GameManager, space_id: str) -> TitleDeed:
    space = manager.board.find_space_by_id(space_id)
    assert isinstance(space, TitleDeed)
    return space


def test_handle_action_buy_property_keeps_payload_and_state_changes() -> None:
    """BUY_PROPERTY keeps event shape and mutates player/deed state."""
    manager = _make_manager_with_two_players()

    result = manager.handle_action("BUY_PROPERTY", "p1", "med_ave")

    assert result == {
        "type": "property_bought",
        "player_id": "p1",
        "space_id": "med_ave",
        "price": 60,
    }

    player = manager.players[0]
    deed = _get_ownable_space(manager, "med_ave")
    assert player.cash == 1440
    assert player.property_ids == ["med_ave"]
    assert deed.owner_id == "p1"


def test_handle_action_decline_property_keeps_event_shape() -> None:
    """DECLINE_PROPERTY keeps start_auction payload contract."""
    manager = _make_manager_with_two_players()

    result = manager.handle_action("DECLINE_PROPERTY", "p1", "med_ave")

    assert result == {
        "type": "start_auction",
        "player_id": "p1",
        "space_id": "med_ave",
        "starting_price": 1,
    }


def test_handle_action_raises_when_property_already_owned() -> None:
    """Owned property path still raises ValueError for follow-up actions."""
    manager = _make_manager_with_two_players()
    owner = manager.players[0]
    deed = _get_ownable_space(manager, "reading_rr")
    owner.property_ids.append("reading_rr")
    deed.owner_id = owner.id

    with pytest.raises(ValueError, match="Property already owned"):
        manager.handle_action("BUY_PROPERTY", "p2", "reading_rr")


def test_land_on_space_owned_railroad_keeps_rent_paid_shape() -> None:
    """Landing on owned ownable space still returns rent_paid with space_id."""
    manager = _make_manager_with_two_players()
    owner = manager.players[0]
    payer = manager.players[1]
    owner.property_ids.append("reading_rr")

    railroad = _get_ownable_space(manager, "reading_rr")
    railroad.owner_id = owner.id

    result = manager.land_on_space(railroad, payer)

    assert result == {
        "type": "rent_paid",
        "payer_id": "p2",
        "owner_id": "p1",
        "rent": 25,
        "space_id": "reading_rr",
    }
    assert payer.cash == 1475
    assert owner.cash == 1525
