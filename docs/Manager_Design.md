# Manager Design

Status: Updated post-PR2 (branch: `pr2-ownership-purchases`)

## 1) Purpose and Scope
`GameManager` currently acts as an orchestration facade for game flow while the codebase transitions toward layered architecture.

It is responsible for:
- Turn lifecycle orchestration (start game, run turn, dispatch action handlers)
- Coordinating movement and space-resolution flow
- Delegating rent and deed behavior to model/policy logic

It is **not** intended to permanently own:
- Pure movement/tax/card rules (target: `engine/rules`)
- Multi-entity ownership orchestration (target: `engine/services/ownership.py`)
- Application-level use-case orchestration (target: `application/use_cases`)
- Transport schemas / API payload contracts (target: `schemas` + `mappers`)

## 2) Current Domain Context (post-PR1)
- `GameState` exists as aggregate root (`engine/models/game_state.py`).
- Rent behavior is policy-based (`engine/policies/rent/*`).
- Legacy turn and action flow still resides in `GameManager` while migration is in progress.

## 3) Core State and Invariants
Current state held by manager or adjacent aggregate:
- `board`: Monopoly board spaces
- `players`: ordered player collection
- `index_of_current_player`: index into players list
- `game_phase`: `SETUP | PLAYING | ENDED`
- `end_game`: boolean game-over marker
- `last_dice_roll`: last movement roll, used by utility rent

Invariants:
- Game starts only from `SETUP`.
- Player count must remain within 2..8 at game start.
- Turn execution allowed only in `PLAYING`.
- Property ownership is unique per deed.
- Rent transfers cannot create negative cash; shortfall triggers bankruptcy event.

## 4) Behavioral Responsibilities
### Turn lifecycle
- `start_game()` validates setup and randomizes player order.
- `new_turn()` executes move -> resolve space -> check win -> rotate player index.

### Space resolution
- Ownable spaces branch into: unowned prompt, self-owned no-op, or rent collection.
- Special spaces branch into tax/card/jail outcomes.

### Action handling
- `handle_action()` currently handles buy/decline follow-up on unowned property.
- This behavior is the primary extraction target for PR2.

## 5) Design Direction
Target architecture:
- `engine/models`: entities and aggregate roots
- `engine/policies`: composable behavior (already started with rent policies)
- `engine/rules`: pure, stateless domain functions
- `engine/services`: multi-entity coordination and mutation
- `application/use_cases`: intent-level orchestration

`GameManager` should shrink into a temporary compatibility facade and be eventually removed or minimized.

## 6) PR2 Extraction Boundaries
PR2 **extracted** ownership and purchase concerns from `GameManager` into:
- `engine/services/ownership.py` ✅
- `engine/rules/purchases.py` ✅

Extracted:
- ✅ `_get_owner_of_space` → `find_owner(players, space_id)`
- ✅ `_get_owner_assets` → `collect_owner_assets(board, owner)`
- ✅ `_pay_rent` → `transfer_rent(payer, owner, rent)`
- ✅ `_resolve_unowned_property` → `resolve_unowned_landing(player, deed)`
- ✅ BUY_PROPERTY inline logic → `buy_property(player, deed)`
- ✅ DECLINE_PROPERTY inline logic → `decline_property(player, deed)`

Remaining out of scope (future PRs):
- API endpoint contracts
- Request/response schema redesign
- Full turn orchestration redesign
- Tax, card, and jail space extraction

## 7) Canonical Event Payloads (Compatibility)
Keep payloads backward-compatible while refactoring:
- `rent_paid`: `{type, payer_id, owner_id, rent, space_id}`
- `player_bankrupt`: `{type, payer_id, owner_id, rent_due, paid, shortfall, space_id}`
- `buy_or_auction`: `{type, player_id, space_id, price}`
- `property_bought`: `{type, player_id, space_id, price}`
- `insufficient_funds`: `{type, player_id, space_id, required, cash}`
- `start_auction`: `{type, player_id, space_id, starting_price}`

## 8) Risks and Mitigations
Risks:
- Event shape drift during extraction
- Duplicate ownership logic between manager and new services
- Merge conflicts while PR1/PR2 evolve

Mitigations:
- Shared contract-first approach in docs
- Adapter-style calls from `GameManager` to new modules
- Focused tests per outcome event and mutation side-effect
