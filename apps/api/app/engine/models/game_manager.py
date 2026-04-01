"""Game flow manager for turn order, movement, and space outcomes."""

import random
from dataclasses import dataclass
from enum import StrEnum

from .board import Board
from .board_skeleton import get_board_spaces
from .player import Player
from .space import Space, SpaceType
from .title_deed import TitleDeed


class GamePhase(StrEnum):
    """Lifecycle phases for a Monopoly game session."""

    SETUP = "setup"
    PLAYING = "playing"
    ENDED = "ended"


@dataclass
class GameManager:
    """Coordinate game state transitions and player actions."""

    MIN_PLAYERS = 2
    MAX_PLAYERS = 8

    board: Board
    players: list[Player]
    index_of_current_player: int = 0
    game_phase: GamePhase = GamePhase.SETUP
    end_game: bool = False
    last_dice_roll: int = 0

    @classmethod
    def create_game(cls, player_names: list[str]) -> GameManager:
        """Create a new game manager with a standard board and players."""
        spaces = get_board_spaces()
        board = Board(spaces, "Monopoly")
        players = [Player(id=str(i), name=name) for i, name in enumerate(player_names)]
        return cls(board, players)

    def start_game(self) -> dict | None:
        """Validate setup requirements, randomize order, and begin play."""
        if self.game_phase != GamePhase.SETUP:
            error_message = "Game has already started or ended."
            raise ValueError(error_message)
        if not (self.MIN_PLAYERS <= len(self.players) <= self.MAX_PLAYERS):
            error_message = "Game needs between 2 and 8 players."
            raise ValueError(error_message)

        random.shuffle(self.players)
        self.game_phase = GamePhase.PLAYING
        return self.new_turn()

    def new_turn(self) -> dict | None:
        """Advance one turn for the current player and return the outcome."""
        if self.game_phase != GamePhase.PLAYING:
            error_message = "Cannot play a turn when game is not in PLAYING phase."
            raise ValueError(error_message)

        curr_player = self.players[self.index_of_current_player]
        space = self.move_player(curr_player)
        result = self.land_on_space(space, curr_player)
        self.check_win()

        self.index_of_current_player = (self.index_of_current_player + 1) % len(
            self.players,
        )

        return result

    def move_player(self, player: Player) -> Space:
        """Roll dice, move a player, and return the destination space."""
        first_die = random.randint(1, 6)  # noqa: S311 - non-cryptographic game RNG is intentional
        second_die = random.randint(1, 6)  # noqa: S311 - non-cryptographic game RNG is intentional
        dice_result = first_die + second_die
        self.last_dice_roll = dice_result
        old_position = player.position
        player.position = (player.position + dice_result) % 40
        if player.position < old_position:
            player.cash += 200
        return self.board.get_space_at(player.position)

    def land_on_space(self, space: Space, player: Player) -> dict | None:
        """Resolve effects when a player lands on a specific board space."""
        if space.type in (SpaceType.PROPERTY, SpaceType.STATION, SpaceType.UTILITY):
            return self._handle_ownable_space(space, player)

        if space.id in {"go", "free_parking"}:
            return None

        result: dict | None
        if space.id == "income_tax":
            result = self._handle_tax(
                space,
                player,
                amount=200,
                tax_type="income_tax_paid",
            )
        elif space.id == "luxury_tax":
            result = self._handle_tax(
                space,
                player,
                amount=100,
                tax_type="luxury_tax_paid",
            )
        elif space.id.startswith("chance"):
            result = self._handle_draw_card(
                space,
                player,
                card_type="draw_chance",
            )
        elif space.id.startswith("community_chest"):
            result = self._handle_draw_card(
                space,
                player,
                card_type="draw_community_chest",
            )
        elif space.id == "go_to_jail":
            result = self._handle_go_to_jail(space, player)
        elif space.id == "jail":
            result = self._handle_jail(space, player)
        else:
            result = None

        return result

    def _handle_ownable_space(self, space: Space, player: Player) -> dict | None:
        owner = self._get_owner_of_space(space.id)
        title_deed = self._as_title_deed(space)

        if owner is None:
            return self._resolve_unowned_property(player, title_deed)

        if owner.id == player.id:
            return None

        owner_assets = self._get_owner_assets(owner)
        rent = title_deed.calculate_rent(self.last_dice_roll, owner_assets)
        rent_result = self._pay_rent(player, owner, rent)
        rent_result["space_id"] = title_deed.id
        return rent_result

    def _as_title_deed(self, space: Space) -> TitleDeed:
        if not isinstance(space, TitleDeed):
            error_message = (
                f"Expected TitleDeed for ownable space, got {type(space).__name__}"
            )
            raise TypeError(error_message)
        return space

    def _handle_tax(
        self,
        space: Space,
        player: Player,
        amount: int,
        tax_type: str,
    ) -> dict:
        player.cash -= amount
        return {
            "type": tax_type,
            "player_id": player.id,
            "space_id": space.id,
            "amount": amount,
        }

    def _handle_draw_card(self, space: Space, player: Player, card_type: str) -> dict:
        return {
            "type": card_type,
            "player_id": player.id,
            "space_id": space.id,
        }

    def _handle_go_to_jail(self, space: Space, player: Player) -> dict:
        player.position = 10
        player.in_jail = True
        player.jail_turns = 0
        return {
            "type": "sent_to_jail",
            "player_id": player.id,
            "space_id": space.id,
            "jail_position": 10,
        }

    def _handle_jail(self, space: Space, player: Player) -> dict:
        if player.in_jail:
            return {
                "type": "jail_turn_required",
                "player_id": player.id,
                "jail_turns": player.jail_turns,
            }
        return {
            "type": "just_visiting",
            "player_id": player.id,
            "space_id": space.id,
        }

    def _get_owner_of_space(self, space_id: str) -> Player | None:
        for player in self.players:
            if space_id in player.property_ids:
                return player
        return None

    def _get_owner_assets(self, owner: Player) -> list[TitleDeed]:
        assets: list[TitleDeed] = []
        for property_id in owner.property_ids:
            owned_space = self.board.find_space_by_id(property_id)
            if isinstance(owned_space, TitleDeed):
                assets.append(owned_space)
        return assets

    def _pay_rent(self, player: Player, owner: Player, rent: int) -> dict:
        if rent <= 0:
            return {
                "type": "no_rent_due",
                "payer_id": player.id,
                "owner_id": owner.id,
                "rent": 0,
            }

        if player.cash >= rent:
            player.cash -= rent
            owner.cash += rent
            return {
                "type": "rent_paid",
                "payer_id": player.id,
                "owner_id": owner.id,
                "rent": rent,
            }

        paid = player.cash
        owner.cash += paid
        player.cash = 0
        player.is_bankrupt = True
        return {
            "type": "player_bankrupt",
            "payer_id": player.id,
            "owner_id": owner.id,
            "rent_due": rent,
            "paid": paid,
            "shortfall": rent - paid,
        }

    def _resolve_unowned_property(self, player: Player, space: TitleDeed) -> dict:
        return {
            "type": "buy_or_auction",
            "player_id": player.id,
            "space_id": space.id,
            "price": space.purchase_price,
        }

    def handle_action(self, action_type: str, player_id: str, space_id: str) -> dict:
        """Apply a follow-up action like buying or declining a property."""
        player = self._get_player_by_id(player_id)
        space = self._get_ownable_space(space_id)

        if self._get_owner_of_space(space_id) is not None:
            error_message = "Property already owned."
            raise ValueError(error_message)

        if action_type == "BUY_PROPERTY":
            if player.cash < space.purchase_price:
                return {
                    "type": "insufficient_funds",
                    "player_id": player.id,
                    "space_id": space.id,
                    "required": space.purchase_price,
                    "cash": player.cash,
                }
            player.cash -= space.purchase_price
            player.property_ids.append(space.id)
            space.owner_id = player.id
            return {
                "type": "property_bought",
                "player_id": player.id,
                "space_id": space.id,
                "price": space.purchase_price,
            }

        if action_type == "DECLINE_PROPERTY":
            return {
                "type": "start_auction",
                "player_id": player.id,
                "space_id": space.id,
                "starting_price": 1,
            }

        error_message = f"Unknown action type: {action_type}"
        raise ValueError(error_message)

    def check_win(self) -> Player | None:
        """Return the winner when one active player remains, otherwise None."""
        active_players = [player for player in self.players if not player.is_bankrupt]
        if len(active_players) == 1:
            self.game_phase = GamePhase.ENDED
            self.end_game = True
            return active_players[0]
        return None

    def _get_player_by_id(self, player_id: str) -> Player:
        for player in self.players:
            if player.id == player_id:
                return player
        error_message = f"Player not found: {player_id}"
        raise ValueError(error_message)

    def _get_ownable_space(self, space_id: str) -> TitleDeed:
        space = self.board.find_space_by_id(space_id)
        if not isinstance(space, TitleDeed):
            error_message = f"Space is not ownable: {space_id}"
            raise TypeError(error_message)
        return space
