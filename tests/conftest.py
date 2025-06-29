import pytest
from infrastructure.persistence.repository_impl import ClientRepositoryImpl, ReservationRepositoryImpl
from application.use_cases.create_account import CreateAccount
from application.use_cases.top_up_wallet import TopUpWallet
from application.use_cases.view_rooms import ViewRooms
from application.use_cases.make_reservation import MakeReservation
from application.use_cases.confirm_reservation import ConfirmReservation
from application.use_cases.cancel_reservation import CancelReservation
from application.use_cases.pay_deposit import PayDeposit

@pytest.fixture
def client_repo():
    return ClientRepositoryImpl()

@pytest.fixture
def reservation_repo():
    return ReservationRepositoryImpl()

@pytest.fixture
def create_account_uc(client_repo):
    return CreateAccount(client_repo)

@pytest.fixture
def top_up_wallet_uc(client_repo):
    return TopUpWallet(client_repo)

@pytest.fixture
def view_rooms_uc():
    return ViewRooms()

@pytest.fixture
def make_reservation_uc(reservation_repo):
    return MakeReservation(reservation_repo)

@pytest.fixture
def confirm_reservation_uc(reservation_repo):
    return ConfirmReservation(reservation_repo)

@pytest.fixture
def cancel_reservation_uc(reservation_repo):
    return CancelReservation(reservation_repo)

@pytest.fixture
def pay_deposit_uc(reservation_repo, client_repo):
    return PayDeposit(reservation_repo, client_repo)
