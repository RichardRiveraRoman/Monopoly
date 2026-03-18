from dataclasses import dataclass, field
"""Game engine domain models."""
from .board import Board
from .game_controller import GameController
from .player import Player
from .property import Property
from .space import Space, SpaceColor, SpaceType
from .title_deed import TitleDeed
from .board_skeleton import get_board_spaces
import random

@dataclass
class GameController:
    def __init__(self, board: Board, players: list[Player], index_of_current_player: int):
        self.board = board
        self.players = players
        self.index_of_current_player = index_of_current_player
        self.phase = ''
        game_over: bool = False
        winner: Player | None = None
        current_dice_roll: int | None = None
        
        
        
    def create_game(cls, player_names: list[str]) -> GameController:
        #Factory method bc returns instance of its class
        #initialize board from skeleton file
        spaces = get_board_spaces()
        board = Board(spaces, "Monopoly")
        #make Players
        players = [Player(id=str(i), name=name) for i, name in enumerate(player_names)]
        #return new game controller instance
        return cls(board, players, index_of_current_player = 0)
       
        
    def start_game()
        #
    def move_player()
    def land_on_space()
    def new_turn()
    def check_win()
    
        
      
    
    
    
class GamePhase(StrEnum):
    SETUP = "setup"
    MOVING = "moving"
    LANDING = "landing"
    ENDED = "ended"