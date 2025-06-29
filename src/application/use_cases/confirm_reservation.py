from domain.repositories import ReservationRepository

class ConfirmReservation:
    def __init__(self, reservation_repo):
        self.reservation_repo = reservation_repo

    def execute(self, reservation_id):
        reservation = self.reservation_repo.get(reservation_id)
        if not reservation:
            raise ValueError('Reservation not found')
        balance = reservation.confirm()
        self.reservation_repo.update(reservation)
        return balance
