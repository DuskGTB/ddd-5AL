from __future__ import annotations
from typing import Optional
from domain.repositories import ClientRepository, ReservationRepository
from domain.model.client import Client
from domain.model.reservation import Reservation
from domain.model.value_objects import ClientId, ReservationId, Money, Currency, PhoneNumber
from infrastructure.persistence.models import ClientORM, ReservationORM, RoomORM, reservation_room
from infrastructure.persistence.database import SessionLocal
from domain.model.room import ROOM_CATALOG, RoomType, Room

class ClientRepositoryImpl(ClientRepository):
    def __init__(self):
        self.db = SessionLocal()

    def add(self, client: Client) -> None:
        orm = self.db.query(ClientORM).get(str(client.id))
        if not orm:
            orm = ClientORM(
                id=str(client.id),
                name=client.name,
                email=client.email,
                phone=client.phone.number,
                balance=client.wallet.balance.amount
            )
            self.db.add(orm)
        else:
            orm.name = client.name
            orm.balance = client.wallet.balance.amount
        self.db.commit()

    def get(self, client_id: ClientId) -> Optional[Client]:
        orm = self.db.query(ClientORM).get(str(client_id))
        if not orm:
            return None
        from domain.model.wallet import Wallet
        return Client(
            id=ClientId(orm.id),
            name=orm.name,
            email=orm.email,
            phone=PhoneNumber(number=orm.phone),
            wallet=Wallet(balance=Money(amount=orm.balance, currency=Currency.EUR))
        )

    def get_by_email(self, email: str) -> Optional[Client]:
        orm = self.db.query(ClientORM).filter_by(email=email).first()
        if not orm:
            return None
        from domain.model.wallet import Wallet
        return Client(
            id=ClientId(orm.id),
            name=orm.name,
            email=orm.email,
            phone=PhoneNumber(number=orm.phone),
            wallet=Wallet(balance=Money(amount=orm.balance, currency=Currency.EUR))
        )

class ReservationRepositoryImpl(ReservationRepository):
    def __init__(self):
        self.db = SessionLocal()

    def add(self, reservation: Reservation) -> None:
        orm = self.db.query(ReservationORM).get(str(reservation.id))
        if not orm:
            orm = ReservationORM(
                id=str(reservation.id),
                client_id=str(reservation.client_id),
                checkin_date=reservation.checkin_date,
                nights=reservation.nights,
                total_amount=reservation.total_amount.amount,
                deposit_paid=reservation.deposit_paid,
                confirmed=reservation.confirmed
            )
            self.db.add(orm)
            for room in reservation.rooms:
                room_orm = self.db.query(RoomORM).get(room.type.value)
                if not room_orm:
                    room_orm = RoomORM(type=room.type.value)
                    self.db.add(room_orm)
                orm.rooms.append(room_orm)
        else:
            orm.deposit_paid = reservation.deposit_paid
            orm.confirmed = reservation.confirmed
        self.db.commit()

    def get(self, reservation_id: ReservationId) -> Optional[Reservation]:
        orm = self.db.query(ReservationORM).get(str(reservation_id))
        if not orm:
            return None
        rooms = [
            Room(
                type=RoomType(r.type),
                price_per_night=ROOM_CATALOG[RoomType(r.type)]['price'],
                features=ROOM_CATALOG[RoomType(r.type)]['features']
            )
            for r in orm.rooms
        ]
        return Reservation(
            id=ReservationId(orm.id),
            client_id=ClientId(orm.client_id),
            checkin_date=orm.checkin_date,
            nights=int(orm.nights),
            rooms=rooms,
            total_amount=Money(amount=orm.total_amount, currency=Currency.EUR),
            deposit_paid=orm.deposit_paid,
            confirmed=orm.confirmed
        )

    def update(self, reservation: Reservation) -> None:
        orm = self.db.query(ReservationORM).get(str(reservation.id))
        orm.deposit_paid = reservation.deposit_paid
        orm.confirmed = reservation.confirmed
        self.db.commit()