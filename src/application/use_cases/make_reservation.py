from domain.model.reservation import Reservation
from domain.model.room import Room
from domain.repositories import ReservationRepository
from domain.model.value_objects import ClientId

class MakeReservation:
    def __init__(self, reservation_repo: ReservationRepository):
        self.reservation_repo = reservation_repo

    def execute(self, client_id: str, checkin_date, nights: int, rooms: list[Room]) -> Reservation:

        cid = ClientId(client_id)
        reservation = Reservation.create(cid, checkin_date, nights, rooms)
        self.reservation_repo.add(reservation)
        return reservation