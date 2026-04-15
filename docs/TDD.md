# Technical Design Document (TDD)

Project: Monopoly API Engine Refactor  
Focus: PR2 (Ownership + Purchases extraction)  
Date: 2026-04-15  
Status: **IMPLEMENTED** — all acceptance criteria met, lint + 14 tests green

## 1) Objective
Extract ownership and purchase concerns from `GameManager` into dedicated domain modules while preserving existing behavior and event payload compatibility.

## 2) Context
PR1 established foundational architecture work:
- Added `GameState` aggregate root
- Introduced rent policies under `engine/policies/rent`

Current pain point:
- `GameManager` still mixes orchestration, state mutation, ownership rules, and action resolution.

## 3) Scope
### In Scope (PR2)
- Introduce `engine/services/ownership.py`
- Introduce `engine/rules/purchases.py`
- Route `GameManager` ownership and buy/decline paths through new modules
- Preserve current output event shapes and exception behavior

### Out of Scope
- API endpoint redesign
- New persistence layer
- Full migration to application use-cases
- Tax/card/jail extraction (future PR)

## 4) Proposed Design

### 4.1 Ownership Service (`engine/services/ownership.py`)
Service coordinates multi-entity ownership behavior.

Proposed functions:
- `find_owner(players, space_id) -> Player | None`
- `collect_owner_assets(board, owner) -> list[TitleDeed]`
- `transfer_rent(payer, owner, rent) -> dict`

Behavioral notes:
- `transfer_rent` returns `no_rent_due`, `rent_paid`, or `player_bankrupt`
- Bankruptcy path transfers remaining cash, sets payer cash to 0, marks bankrupt

### 4.2 Purchase Rules (`engine/rules/purchases.py`)
Pure-ish domain rule helpers for purchase decisions.

Proposed functions:
- `resolve_unowned_landing(player, deed) -> dict`
- `buy_property(player, deed) -> dict`
- `decline_property(player, deed) -> dict`

Behavioral notes:
- `buy_property` validates affordability and mutates deed ownership + player assets
- `decline_property` emits auction-start event with `starting_price = 1`

### 4.3 Manager Integration
`GameManager` remains compatibility facade.

Changes:
- Replace private ownership helpers with service calls
- Replace BUY/DECLINE inline logic with purchase rule calls
- Keep method signatures and return envelopes stable

## 5) Compatibility Contract
Event payloads must remain backward-compatible for current consumers.

Required event types:
- `buy_or_auction`
- `property_bought`
- `insufficient_funds`
- `start_auction`
- `rent_paid`
- `player_bankrupt`
- `no_rent_due`

## 6) Error Handling Contract
- Unknown action type -> `ValueError`
- Property already owned on buy/decline attempt -> `ValueError`
- Non-ownable space passed to ownable handlers -> `TypeError`

## 7) Testing Strategy
### Unit tests (new modules)
- Ownership: owner lookup, assets collection, rent transfer branches
- Purchases: unowned resolution, buy success, insufficient funds, decline event

### Integration tests (facade)
- `GameManager.handle_action` still returns same event payloads
- Landing on owned ownable space still charges rent using current rent calculation flow

## 8) Rollout Plan
1. ✅ Add ownership service + tests
2. ✅ Add purchases rules + tests
3. ✅ Wire manager to new modules
4. ✅ Run full test suite and lint
5. ✅ Finalize docs and PR notes
6. Submit PR2 with focused diff and migration notes

## 9) Risks
- Merge conflicts with concurrent architecture work
- Hidden coupling to private manager helpers
- Event payload drift across modules

## 10) Risk Mitigations
- Keep manager as adapter during transition
- Validate event payload snapshots in tests
- Rebase frequently on `controller`

## 11) Acceptance Criteria
- ✅ New ownership and purchase modules exist and are covered by tests
- ✅ `GameManager` buy/decline and rent paths delegate to new modules
- ✅ No consumer-visible behavior regressions in event payloads
- ✅ Lint/tests pass in CI

---

## 12) Implementation Notes (Deviations from Plan)

### 12.1 Circular Import in Rent Policies
**Problem:** Importing model types (`Property`, `Railroad`, `Utility`) from `engine.models` into `engine/policies/rent/*.py` created a circular chain:
```
models.__init__ → game_state → board_skeleton → property
  → policies.rent → policies.rent.property → models.Property
```

**Decision:** Replaced all `isinstance(deed, X)` guards in rent policies with `deed.__class__.__name__ == "X"` string checks.  
**Rationale:** Ruff's `PLC0415` rule forbids local imports, ruling out the "import inside function" escape hatch. String-based type dispatch avoids the cycle entirely without weakening correctness for closed-world domain entities.  
**Files affected:** `engine/policies/rent/property.py`, `railroad.py`, `utility.py`

### 12.2 Ruff Configuration
`ruff.toml` required two updates:
- Top-level `select` moved into `[lint]` section (deprecated in newer ruff)
- Added `per-file-ignores` for `tests/*.py` to suppress `S101` (assert) and `PLR2004` (magic value comparisons), which are idiomatic in test code:
```toml
[lint.per-file-ignores]
"tests/*.py" = ["S101", "PLR2004"]
```

### 12.3 Barrel vs. Direct Imports
Using `from app.engine.models import X` (barrel import) in test files triggered the circular import at pytest collection time. All new test files and service modules use direct module-level imports (`from app.engine.models.player import Player`) combined with `TYPE_CHECKING` guards where Ruff's `TC001` rule requires it.

### 12.4 Files Changed
| File | Type | Reason |
|---|---|---|
| `engine/services/ownership.py` | NEW | Ownership coordination service |
| `engine/services/__init__.py` | NEW | Public API for services layer |
| `engine/rules/purchases.py` | NEW | Pure purchase decision rules |
| `engine/rules/__init__.py` | NEW | Public API for rules layer |
| `tests/__init__.py` | NEW | Package marker for pytest |
| `tests/test_ownership_service.py` | NEW | 5 unit tests |
| `tests/test_purchases_rules.py` | NEW | 4 unit tests |
| `tests/test_game_manager_integration.py` | NEW | 4 integration tests |
| `engine/models/game_manager.py` | MODIFIED | Removed 4 private helpers; delegate to new modules |
| `engine/policies/rent/property.py` | MODIFIED | `__class__.__name__` to break circular import |
| `engine/policies/rent/railroad.py` | MODIFIED | Same |
| `engine/policies/rent/utility.py` | MODIFIED | Same |
| `engine/policies/rent/base.py` | MODIFIED | Direct module import for `TitleDeed` |
| `ruff.toml` | MODIFIED | `[lint]` section + per-file-ignores |
