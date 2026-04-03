"""Mapping helpers from domain aggregates to response DTOs."""

from app.engine.models import (
    Board,
    GameState,
    Player,
    Property,
    Railroad,
    Space,
    Utility,
)
from app.schemas.responses import (
    BoardDTO,
    GameStateDTO,
    PlayerDTO,
    PropertyDTO,
    RailroadDTO,
    SpaceDTO,
    SpecialSpaceDTO,
    UtilityDTO,
)


def to_player_dto(player: Player) -> PlayerDTO:
    """Convert a domain player into its API DTO."""
    return PlayerDTO(
        id=player.id,
        name=player.name,
        position=player.position,
        cash=player.cash,
        property_ids=player.property_ids,
        in_jail=player.in_jail,
        jail_turns=player.jail_turns,
        is_bankrupt=player.is_bankrupt,
    )


def to_space_dto(
    space: Space,
) -> SpaceDTO:
    """Convert a domain board space into the matching response DTO."""
    if isinstance(space, Property):
        return PropertyDTO(
            id=space.id,
            name=space.name,
            color=space.color,
            owner_id=space.owner_id,
            purchase_price=space.purchase_price,
            base_rent=space.base_rent,
            is_mortgaged=space.is_mortgaged,
            house_rents=space.house_rents,
            num_houses=space.num_houses,
            house_cost=space.house_cost,
            group_size=space.group_size,
        )

    if isinstance(space, Railroad):
        return RailroadDTO(
            id=space.id,
            name=space.name,
            color=space.color,
            owner_id=space.owner_id,
            purchase_price=space.purchase_price,
            base_rent=space.base_rent,
            is_mortgaged=space.is_mortgaged,
            rent_levels=space.rent_levels,
        )

    if isinstance(space, Utility):
        return UtilityDTO(
            id=space.id,
            name=space.name,
            color=space.color,
            owner_id=space.owner_id,
            purchase_price=space.purchase_price,
            base_rent=space.base_rent,
            is_mortgaged=space.is_mortgaged,
        )

    return SpecialSpaceDTO(
        id=space.id,
        name=space.name,
        color=space.color,
    )


def to_board_dto(board: Board) -> BoardDTO:
    """Convert a domain board into a response DTO."""
    return BoardDTO(
        name=board.name,
        spaces=[to_space_dto(space) for space in board.spaces],
    )


def to_game_state_dto(game_state: GameState) -> GameStateDTO:
    """Convert a domain game-state aggregate into a response DTO."""
    return GameStateDTO(
        id=game_state.id,
        board=to_board_dto(game_state.board),
        players=[to_player_dto(player) for player in game_state.players],
        current_player_index=game_state.index_of_current_player,
        current_player_id=game_state.current_player_id,
        game_phase=game_state.game_phase,
        last_dice_roll=game_state.last_dice_roll,
        end_game=game_state.end_game,
    )
