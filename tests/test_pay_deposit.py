import random
from datetime import date
from application.use_cases.create_account import CreateAccount
from application.use_cases.top_up_wallet import TopUpWallet
from application.use_cases.make_reservation import MakeReservation
from application.use_cases.pay_deposit import PayDeposit
from infrastructure.persistence.repository_impl import ClientRepositoryImpl, ReservationRepositoryImpl
from domain.model.room import Room
from domain.model.value_objects import Money

def test_pay_deposit_flow():
    client_repo = ClientRepositoryImpl()
    reservation_repo = ReservationRepositoryImpl()
    create_uc = CreateAccount(client_repo)
    top_up_uc = TopUpWallet(client_repo)
    make_uc = MakeReservation(reservation_repo)
    pay_uc = PayDeposit(reservation_repo, client_repo)

    rand = random.randint(1_000_000, 9_999_999)
    email = f"dave{rand}@example.com"
    client_id = create_uc.execute("Dave", email, "+33123456782")
    top_up_uc.execute(client_id, 200, "EUR")

    room = Room.all_rooms()[0]
    reservation = make_uc.execute(client_id, date.today(), 1, [room])

    deposit = pay_uc.execute(reservation.id)
    assert isinstance(deposit, Money)
    assert deposit.amount == reservation.total_amount.amount * 0.5

    client = client_repo.get(client_id)
    assert client.wallet.balance.amount == 200 - deposit.amount
