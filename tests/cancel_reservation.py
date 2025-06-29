from domain.repositories import ReservationRepository
from domain.model.value_objects import ReservationId

class CancelReservation:
    def __init__(self, reservation_repo: ReservationRepository):
        self.reservation_repo = reservation_repo

    def execute(self, reservation_id: str) -> None:
        rid = ReservationId(reservation_id)
        reservation = self.reservation_repo.get(rid)
        if not reservation:
            return
        reservation.cancel()
        self.reservation_repo.update(reservation)
