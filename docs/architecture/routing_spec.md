# Frontend Routing Spec (MVP)

Status: Draft

## Purpose
Define the minimum route structure for the web client so Lobby and Game Room can be built on a stable URL contract.

## Route Table

| Route | Purpose | Notes |
| --- | --- | --- |
| `/` | Entry point | Redirect to `/lobby` |
| `/lobby` | Create/join game screen | Pre-game interactions |
| `/game/:gameId` | Active game room | `gameId` is required |
| `*` | Fallback | Redirect to `/lobby` |

## URL Contract

### `/lobby`
- No required route params.
- Actions:
	- Create game -> navigate to `/game/:gameId`
	- Join game by ID -> navigate to `/game/:gameId`
- API dependencies:
	- Planned: `POST /games` to create a new game and receive `gameId`.
	- Planned: `GET /games/:gameId` to validate a user-entered game ID before navigation.
	- Current implementation: only `GET /` exists.

### `/game/:gameId`
- Required param: `gameId`.
- Behavior:
	- Fetch/load game state for `gameId`.
	- If not found or invalid, show recoverable error and offer navigation to `/lobby`.
- API dependencies:
	- Planned: `GET /games/:gameId` to load game room state on initial render/refresh.
	- Planned: `POST /games/:gameId/actions` to submit player actions (buy, decline, etc.).
	- Current implementation: only `GET /` exists.

## State Boundaries

### URL-owned state
- `gameId`

### UI/local state
- Form inputs (player name, game ID field)
- Loading and error flags
- Temporary view-only toggles

### API/domain-owned state
- Turn state
- Board state
- Player cash/properties
- Game phase

## Navigation Rules
- App start at `/` always redirects to `/lobby`.
- Unknown routes redirect to `/lobby`.
- Refreshing `/game/:gameId` preserves route context and attempts reload.

## Error Handling (MVP)
- Invalid `gameId`: render lightweight "Game not found" state with "Back to Lobby" action.
- API/network failure in Game Room: show retry option while staying on same route.

## Acceptance Criteria
- Visiting `/` lands user on Lobby.
- Visiting `/lobby` shows pre-game view.
- Visiting `/game/abc123` initializes Game Room for `abc123`.
- Invalid game route produces recoverable not-found state.
- Unknown route (for example `/foo`) redirects to `/lobby`.
