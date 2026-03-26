import random
from dataclasses import dataclass, field
from enum import StrEnum

from .board import Board
from .board_skeleton import get_board_spaces
from .player import Player
from .space import Space, SpaceType
from .title_deed import TitleDeed


class GamePhase(StrEnum):
    SETUP = "setup"
    PLAYING = "playing"
    ENDED = "ended"


@dataclass
class GameManager:
    board: Board
    players: list[Player]
    index_of_current_player: int = 0
    game_phase: GamePhase = GamePhase.SETUP
    end_game: bool = False
    last_dice_roll: int = 0

    @classmethod
    def create_game(cls, player_names: list[str]) -> "GameManager":
        spaces = get_board_spaces()
        board = Board(spaces, "Monopoly")
        players = [Player(id=str(i), name=name) for i, name in enumerate(player_names)]
        return cls(board, players)

    def start_game(self) -> dict | None:
        if self.game_phase != GamePhase.SETUP:
            raise ValueError("Game has already started or ended.")
        if not (2 <= len(self.players) <= 8):
            raise ValueError("Game needs between 2 and 8 players.")

        random.shuffle(self.players)
        self.game_phase = GamePhase.PLAYING
        return self.new_turn()

    def new_turn(self) -> dict | None:
        if self.game_phase != GamePhase.PLAYING:
            raise ValueError("Cannot play a turn when game is not in PLAYING phase.")

        curr_player = self.players[self.index_of_current_player]
        space = self.move_player(curr_player)
        result = self.land_on_space(space, curr_player)
        self.check_win()

        self.index_of_current_player = (self.index_of_current_player + 1) % len(
            self.players
        )

        return result

    def move_player(self, player: Player) -> Space:
        dice_result = random.randint(1, 6) + random.randint(1, 6)
        self.last_dice_roll = dice_result
        old_position = player.position
        player.position = (player.position + dice_result) % 40
        if player.position < old_position:
            player.cash += 200
        space = self.board.get_space_at(player.position)
        return space

    def land_on_space(self, space: Space, player: Player) -> dict | None:
        if space.type in (SpaceType.PROPERTY, SpaceType.STATION, SpaceType.UTILITY):
            owner = self._get_owner_of_space(space.id)
            if owner is None:
                if not isinstance(space, TitleDeed):
                    raise TypeError(
                        f"Expected TitleDeed for ownable space, got {type(space).__name__}"
                    )
                return self._resolve_unowned_property(player, space)

            if owner.id == player.id:
                return None

            if not isinstance(space, TitleDeed):
                raise TypeError(
                    f"Expected TitleDeed for ownable space, got {type(space).__name__}"
                )

            owner_assets = self._get_owner_assets(owner)
            rent = space.calculate_rent(self.last_dice_roll, owner_assets)
            rent_result = self._pay_rent(player, owner, rent)
            rent_result["space_id"] = space.id
            return rent_result

        if space.id == "go":
            return None

        if space.id == "income_tax":
            player.cash -= 200
            return {
                "type": "income_tax_paid",
                "player_id": player.id,
                "space_id": space.id,
                "amount": 200,
            }

        if space.id == "luxury_tax":
            player.cash -= 100
            return {
                "type": "luxury_tax_paid",
                "player_id": player.id,
                "space_id": space.id,
                "amount": 100,
            }

        if space.id.startswith("chance"):
            return {
                "type": "draw_chance",
                "player_id": player.id,
                "space_id": space.id,
            }

        if space.id.startswith("community_chest"):
            return {
                "type": "draw_community_chest",
                "player_id": player.id,
                "space_id": space.id,
            }

        if space.id == "go_to_jail":
            player.position = 10
            player.in_jail = True
            player.jail_turns = 0
            return {
                "type": "sent_to_jail",
                "player_id": player.id,
                "space_id": space.id,
                "jail_position": 10,
            }

        if space.id == "jail":
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

        if space.id == "free_parking":
            return None

        return None

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
        player = self._get_player_by_id(player_id)
        space = self._get_ownable_space(space_id)

        if self._get_owner_of_space(space_id) is not None:
            raise ValueError("Property already owned.")

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

        raise ValueError(f"Unknown action type: {action_type}")

    def check_win(self) -> Player | None:
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
        raise ValueError(f"Player not found: {player_id}")

    def _get_ownable_space(self, space_id: str) -> TitleDeed:
        space = self.board.find_space_by_id(space_id)
        if not isinstance(space, TitleDeed):
            raise ValueError(f"Space is not ownable: {space_id}")
        return space
