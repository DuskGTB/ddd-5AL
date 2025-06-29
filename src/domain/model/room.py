from __future__ import annotations
from enum import Enum
from pydantic import BaseModel
from .value_objects import Money

class RoomType(str, Enum):
    STANDARD = "standard"
    SUPERIOR = "superior"
    SUITE = "suite"

ROOM_CATALOG: dict[RoomType, dict] = {
    RoomType.STANDARD:  {'price': Money(amount=50),  'features': ['Lit 1 place', 'Wifi', 'TV']},
    RoomType.SUPERIOR:   {'price': Money(amount=100), 'features': ['Lit 2 places', 'Wifi', 'TV ecran plat', 'Minibar', 'Climatiseur']},
    RoomType.SUITE:      {'price': Money(amount=200), 'features': ['Lit 2 places', 'Wifi', 'TV ecran plat', 'Minibar', 'Climatiseur', 'Baignoire', 'Terrasse']},
}

class Room(BaseModel):
    type: RoomType
    price_per_night: Money
    features: list[str]

    @classmethod
    def all_rooms(cls) -> list[Room]:
        return [
            cls(type=rt, price_per_night=data['price'], features=data['features'])
            for rt, data in ROOM_CATALOG.items()
        ]