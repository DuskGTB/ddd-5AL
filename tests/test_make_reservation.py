import random
from datetime import date
from application.use_cases.create_account import CreateAccount
from application.use_cases.make_reservation import MakeReservation
from infrastructure.persistence.repository_impl import ClientRepositoryImpl, ReservationRepositoryImpl
from domain.model.room import Room

def test_make_reservation():
    client_repo = ClientRepositoryImpl()
    reservation_repo = ReservationRepositoryImpl()
    create_uc = CreateAccount(client_repo)
    make_uc = MakeReservation(reservation_repo)

    rand = random.randint(1_000_000, 9_999_999)
    email = f"carol{rand}@example.com"
    client_id = create_uc.execute("Carol", email, "+33123456781")
    room = Room.all_rooms()[0]
    reservation = make_uc.execute(client_id, date.today(), 1, [room])
    assert reservation.total_amount.amount > 0
