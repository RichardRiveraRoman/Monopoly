"""Title deed model for ownable board spaces."""

from dataclasses import dataclass

from .space import Space


@dataclass
class TitleDeed(Space):
    """A Space that can be owned, bought, and rented."""

    owner_id: str | None = None
    purchase_price: int = 0
    base_rent: int = 0
    mortgage_value: int = 0
    is_mortaged: bool = False
