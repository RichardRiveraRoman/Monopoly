# Monopoly Manager Design

Status: Draft (updated to match current `GameManager` implementation)

## 1) Purpose and Scope
`GameManager` coordinates turn flow and high-level game decisions.

It is responsible for:
- Creating an in-memory game session (`create_game`)
- Validating and starting play (`start_game`)
- Running turn progression (`new_turn`)
- Resolving what happens when a player lands on a space (`land_on_space`)
- Handling follow-up property actions (`handle_action`)
- Determining win state (`check_win`)

It is not responsible for:
- Persistence/storage
- HTTP API transport concerns
- UI concerns

## 2) Core State
- `board: Board`
- `players: list[Player]`
- `index_of_current_player: int`
- `game_phase: GamePhase` (`SETUP`, `PLAYING`, `ENDED`)
- `end_game: bool`
- `last_dice_roll: int`
- `MIN_PLAYERS = 2`, `MAX_PLAYERS = 8`

Notes:
- Ownership is inferred from each player's `property_ids`.
- Game manager does not maintain separate ownership maps.

## 3) Public Methods

### `create_game(player_names)`
- Builds board from `get_board_spaces()`
- Creates players with string IDs based on index
- Returns initialized `GameManager` in `SETUP`

### `start_game()`
- Validates `game_phase == SETUP`
- Validates player count between 2 and 8 inclusive
- Randomizes player order
- Sets phase to `PLAYING`
- Immediately executes first turn via `new_turn()`

### `new_turn()`
- Validates `game_phase == PLAYING`
- Gets current player by `index_of_current_player`
- Moves player via `move_player()`
- Resolves space via `land_on_space()`
- Calls `check_win()`
- Advances current player index (round-robin)
- Returns turn result event dictionary or `None`

### `move_player(player)`
- Rolls 2d6 using `random.randint`
- Stores roll in `last_dice_roll`
- Moves position modulo 40
- Awards $200 when passing GO
- Returns destination `Space`

### `land_on_space(space, player)`
- Ownable spaces (`PROPERTY`, `STATION`, `UTILITY`) delegate to `_handle_ownable_space`
- GO / Free Parking => no event (`None`)
- Income tax / luxury tax => cash deduction + tax event
- Chance / Community Chest => draw event markers
- Go To Jail => send player to jail and emit jail event
- Jail => `jail_turn_required` if in jail, else `just_visiting`

### `handle_action(action_type, player_id, space_id)`
- Validates target property is not already owned
- `BUY_PROPERTY`: buys if cash sufficient, else returns `insufficient_funds`
- `DECLINE_PROPERTY`: returns `start_auction`
- Unknown action raises `ValueError`

### `check_win()`
- Filters active (non-bankrupt) players
- If one remains: sets phase to `ENDED`, sets `end_game = True`, returns winner
- Else returns `None`

## 4) Key Internal Helpers
- `_handle_ownable_space(space, player)`
- `_as_title_deed(space)`
- `_handle_tax(space, player, amount, tax_type)`
- `_handle_draw_card(space, player, card_type)`
- `_handle_go_to_jail(space, player)`
- `_handle_jail(space, player)`
- `_get_owner_of_space(space_id)`
- `_get_owner_assets(owner)`
- `_pay_rent(player, owner, rent)`
- `_resolve_unowned_property(player, space)`
- `_get_player_by_id(player_id)`
- `_get_ownable_space(space_id)`

## 5) Event Shapes Returned by Manager
Manager methods return dictionaries (or `None`) as game events. Common event `type` values:
- `buy_or_auction`
- `rent_paid`, `player_bankrupt`, `no_rent_due`
- `income_tax_paid`, `luxury_tax_paid`
- `draw_chance`, `draw_community_chest`
- `sent_to_jail`, `jail_turn_required`, `just_visiting`
- `property_bought`, `insufficient_funds`, `start_auction`

## 6) Current Constraints / Follow-ups
- No persistence layer integration yet
- No auction resolution logic yet (only start signal)
- No card deck resolution yet (only draw signal)
- Uses simple non-cryptographic randomness for gameplay (intentional)