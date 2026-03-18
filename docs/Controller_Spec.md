Technical Design Document (TDD): Monopoly Game Controller Design
Status: Draft | Author: Peter J. Limburg | Co-written with GitHub CoPilot

1. Purpose and Scope of Game Controller
Logic for managing Monopoly game state, player turns, and game flow.


2. State Variables
players: Ordered list of Player objects
board: Board object
index_of_current_player: int tracking whose turn it is
game_phase: enum tracking high-level phase of game
game_over: Check for winner
turn_history: List of events
available_pieces: 
     

3. Methods
create_game(players): Initialize game, set starting money
start_game(): Randomize player order, set phase to playing
advance_to_next_turn(): Move to next turn's player
end_game(): Set phase to ended
get_current_player(): Return Player for index_of_current_player
handle_action(): Process Player actions (Move, buy, sell, etc.)
move_player(): Roll dice, move current player by rolled amount
land_on_space(): Trigger effect of space


4. Relationships to other models
Controller -> Player
Controller -> Board



5. Example state transitions and flow
    ok. 


Detailed descriptions for each state variable and method (what, why, how).
Edge cases and error handling (e.g., what happens if a player disconnects, or tries to buy with insufficient funds).
Example flows for common actions (e.g., a full turn, buying property, auction).

---

### State Variable: players
- **What:**
  - Ordered list of Player objects representing all participants in the current game session.
- **Why:**
  - The order determines turn sequence and is needed for tracking whose turn it is, resolving actions, and managing game flow.
- **How:**
  - Initialized in create_game by instantiating Player objects for each player name provided.
  - The order is later randomized, in place, in start_game to determine play order.
  - Accessed throughout the game to get player state, update balances, move pieces, etc.
### State Variable: board
- **What:**
    - Board object representing all 40 spaces on a Monopoly Board
- **Why:**
    - Centralizes all space information for controller to perform lookups
    - Board does not track ownership; ownership is managed by Player objects.
- **How:**
    - Initialized in create_game by getting 40 spaces and passing them into creation of the Board instance
    - Accessed throughout the game to get space information
### State Variable: index_of_current_player
- **What:**
    - Integer representing index of current player in players 
- **Why:**
    - Tracks index for access to current player
- **How:**
    - Updated every turn in advance_to_next_turn method
### State Variable: 


### Method: create_game(players)
- **What:**
  - Factory method to initialize a new game session, setting up the board and creating Player objects.
- **Why:**
  - Encapsulates all logic needed to start a fresh game, ensuring all required state is set up before play begins.
- **How:**
  - Receives a list of player names as input.
  - Calls get_board_spaces() to create the board.
  - Instantiates Player objects for each name, assigns starting money and default state.
  - Returns a new GameController instance with initialized board, players, and default phase/index values.