from application.use_cases.cancel_reservation import CancelReservation
from infrastructure.persistence.repository_impl import ReservationRepositoryImpl

def test_cancel_reservation():
    reservation_repo = ReservationRepositoryImpl()
    cancel_uc = CancelReservation(reservation_repo)
    cancel_uc.execute("non-existent-id")
