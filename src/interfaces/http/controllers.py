from flask import Blueprint, request, jsonify
from datetime import date
from domain.model.room import Room, RoomType, ROOM_CATALOG
from application.use_cases.create_account import CreateAccount
from application.use_cases.top_up_wallet import TopUpWallet
from application.use_cases.view_rooms import ViewRooms
from application.use_cases.make_reservation import MakeReservation
from application.use_cases.confirm_reservation import ConfirmReservation
from application.use_cases.cancel_reservation import CancelReservation
from application.use_cases.pay_deposit import PayDeposit
from infrastructure.persistence.repository_impl import ClientRepositoryImpl, ReservationRepositoryImpl

router = Blueprint('api', __name__, url_prefix='/api')
client_repo = ClientRepositoryImpl()
reservation_repo = ReservationRepositoryImpl()

create_account_uc = CreateAccount(client_repo)
top_up_wallet_uc = TopUpWallet(client_repo)
view_rooms_uc = ViewRooms()
make_reservation_uc = MakeReservation(reservation_repo)
confirm_reservation_uc = ConfirmReservation(reservation_repo)
cancel_reservation_uc = CancelReservation(reservation_repo)
pay_deposit_uc = PayDeposit(reservation_repo, client_repo)

@router.post('/clients')
def create_client():
    data = request.json
    client_id = create_account_uc.execute(
        name=data['name'], email=data['email'], phone=data['phone']
    )
    return jsonify({'client_id': str(client_id)}), 201

@router.post('/clients/<client_id>/wallet')
def top_up_wallet(client_id):
    data = request.json
    top_up_wallet_uc.execute(client_id, data['amount'], data['currency'])
    return '', 204

@router.get('/rooms')
def list_rooms():
    rooms = view_rooms_uc.execute()
    return jsonify([room.dict() for room in rooms]), 200

@router.post('/reservations')
def make_reservation_route():
    data = request.json
    checkin = date.fromisoformat(data['checkin_date'])
    rooms = [
        Room(
            type=RoomType(rt),
            price_per_night=ROOM_CATALOG[RoomType(rt)]['price'],
            features=ROOM_CATALOG[RoomType(rt)]['features']
        )
        for rt in data['rooms']
    ]
    reservation = make_reservation_uc.execute(
        data['client_id'],
        checkin,
        data['nights'],
        rooms
    )
    return jsonify(reservation.dict()), 201

@router.post('/reservations/<reservation_id>/deposit')
def pay_reservation_deposit(reservation_id):
    amount = pay_deposit_uc.execute(reservation_id)
    return jsonify({'deposit_paid': amount.amount}), 200

@router.post('/reservations/<reservation_id>/confirm')
def confirm_reservation(reservation_id):
    balance = confirm_reservation_uc.execute(reservation_id)
    return jsonify({'balance_due': balance.amount}), 200

@router.post('/reservations/<reservation_id>/cancel')
def cancel_reservation(reservation_id):
    cancel_reservation_uc.execute(reservation_id)
    return '', 204