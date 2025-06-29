from domain.model.client import Client
from domain.model.value_objects import ClientId, PhoneNumber
from domain.model.wallet import Wallet
from domain.repositories import ClientRepository

class CreateAccount:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    def execute(self, name: str, email: str, phone: str) -> ClientId:
        if self.client_repo.get_by_email(email):
            raise ValueError('Email already in use')


        client = Client(
            id=ClientId.new(),
            name=name,
            email=email,             
            phone=PhoneNumber(number=phone),
            wallet=Wallet()
        )
        self.client_repo.add(client)
        return client.id