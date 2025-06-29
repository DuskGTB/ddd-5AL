from __future__ import annotations
from pydantic import BaseModel, validator
from pydantic.config import ConfigDict
from datetime import date
from .value_objects import ReservationId, ClientId, Money
from .room import Room

class Reservation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ReservationId
    client_id: ClientId
    checkin_date: date
    nights: int
    rooms: list[Room]
    total_amount: Money
    deposit_paid: bool = False
    confirmed: bool = False

    @validator('nights')
    def nights_positive(cls, v):
        if v < 1:
            raise ValueError('Au moins une nuit')
        return v

    @classmethod
    def create(cls, client_id: ClientId, checkin_date: date, nights: int, rooms: list[Room]) -> Reservation:
        total = Money(amount=0)
        for room in rooms:
            total += room.price_per_night * nights
        return cls(
            id=ReservationId.new(),
            client_id=client_id,
            checkin_date=checkin_date,
            nights=nights,
            rooms=rooms,
            total_amount=total
        )

    def pay_deposit(self) -> Money:
        if self.deposit_paid:
            raise ValueError('Déjà payé')
        self.deposit_paid = True
        return self.total_amount * 0.5

    def confirm(self) -> Money:
        if not self.deposit_paid:
            raise ValueError('Dépôt non payé')
        if self.confirmed:
            raise ValueError('Déjà confirmé')
        self.confirmed = True
        return self.total_amount * 0.5

    def cancel(self) -> None:
        pass