from domain.repositories import ReservationRepository, ClientRepository
from domain.model.value_objects import ReservationId, Money
from domain.model.reservation import Reservation

class PayDeposit:
    def __init__(self, reservation_repo: ReservationRepository, client_repo: ClientRepository):
        self.reservation_repo = reservation_repo
        self.client_repo = client_repo

    def execute(self, reservation_id: str) -> Money:
        rid = ReservationId(reservation_id)
        reservation = self.reservation_repo.get(rid)
        if not reservation:
            raise ValueError('Reservation not found')
        deposit_amount = reservation.pay_deposit()
        client = self.client_repo.get(reservation.client_id)
        if not client:
            raise ValueError('Client not found')
        client.wallet.debit(deposit_amount)
        self.client_repo.add(client)
        self.reservation_repo.update(reservation)
        return deposit_amount