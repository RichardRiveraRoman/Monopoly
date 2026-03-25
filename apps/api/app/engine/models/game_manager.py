from dataclasses import dataclass, field
"""Game engine domain models."""
from .board import Board
from .game_manager import GameController
from .player import Player
from .property import Property
from .space import Space, SpaceColor, SpaceType
from .title_deed import TitleDeed
from .board_skeleton import get_board_spaces
import random
from enum import StrEnum 
from .board import Board

class GamePhase(StrEnum):
    SETUP = "setup"
    PLAYING = "playing"
    ENDED = "ended"
    
@dataclass
class GameManager:
    def __init__(self, board: Board, players: list[Player]):
        self.board = board
        self.players = players
        self.index_of_current_player = 0
        self.game_phase = GamePhase.SETUP
        self.end_game = False

        
        
        
    def create_game(cls, player_names: list[str]) -> GameController:
        #Factory method bc returns instance of its class
        #initialize board from skeleton file
        spaces = get_board_spaces()
        board = Board(spaces, "Monopoly")
        #make Players
        players = [Player(id=str(i), name=name) for i, name in enumerate(player_names)]
        #return new game controller instance
        return cls(board, players)
       
        
    def start_game(self):
        if self.game_phase != GamePhase.SETUP :
            raise ValueError("Game has already started or ended.")
        if not (2 <= len(self.players) <= 8):
            raise ValueError("Game needs between 2 and 8 players.")
        
        random.shuffle(self.players)
        self.game_phase = GamePhase.PLAYING
        self.new_turn()
    
    
    def new_turn(self):
        curr_player = self.players[self.index_of_current_player]
        space = self.move_player(curr_player)
        self.land_on_space(space, curr_player)
        
        self.index_of_current_player = (self.index_of_current_player + 1) % len(self.players)
            

    def move_player(self, player: Player) -> str:
        dice_result = random.randint(1, 6) + random.randint(1, 6)        
        old_position = player.position
        player.position = (player.position + dice_result) % 40
        #passed go?
        if player.position < old_position:
            player.cash += 200
        space = self.board.get_space_at(player.position)
        return space
    
    
    def land_on_space(self, space: Space, player: Player):
        if space.type == SpaceType.PROPERTY:
            owner = self._get_owner_of_space(space.id)
            if owner is None:
                return self._resolve_unowned_property(player, space) #asks UI for player's decision
            elif owner.id == player.id:
                return None
            else:
                #player pays rent
                self._pay_rent(player, owner, space)
                return {"type": "rent_paid", "payer_id": player.id, "owner_id": owner.id, "space_id": space.id}
                

        elif space.type == SpaceType.RAILROAD:
        # owned?
        # railroad rent or offer purchase
            pass

        elif space.type == SpaceType.UTILITY:
        # owned?
        # utility rent or offer purchase
            pass

        elif space.type == SpaceType.GO:
            pass

        elif space.type == SpaceType.INCOME_TAX:
            player.cash -= 200

        elif space.type == SpaceType.LUXURY_TAX:
            player.cash -= 100

        elif space.type == SpaceType.CHANCE:
            pass

        elif space.type == SpaceType.COMMUNITY_CHEST:
            pass

        elif space.type == SpaceType.GO_TO_JAIL:
            player.position = 10
            player.in_jail = True

        elif space.type == SpaceType.JAIL:
            pass

        elif space.type == SpaceType.FREE_PARKING:
            pass
            

    def _get_owner_of_space(self, space_id: str) -> Player | None:
        for player in self.players:
            if space_id in player.property_ids: 
                return player
        return None
    
    def _pay_rent()
    
    
    #Step 1 (land_on_space): “Player must choose buy or auction.”
    # Step 2 (handle_action): apply the chosen mutation (BUY_PROPERTY or DECLINE_PROPERTY).
    # Where frontend communication happens. The API layer passes that payload to the frontend and, after the user clicks, sends the selected action back to GameManager via handle_action(...).
    def _resolve_unowned_property(self, player: Player, space: Space) -> dict:
        return {
            "type": "buy_or_auction",
            "player_id": player.id,
            "space_id": space.id,
            "price": space.price,  # or title_deed.price field
        }
    
    def handle_action(self, action_type: str, player_id: str, space_id: str):
        if action_type == "BUY_PROPERTY":
            #...
        elif action_type == "DECLINE_PROPERTY":
            #...
    
    def check_win()
    
        
      
    
    
    
class GamePhase(StrEnum):
    SETUP = "setup"
    MOVING = "moving"
    LANDING = "landing"
    ENDED = "ended"