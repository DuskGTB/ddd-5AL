from domain.model.value_objects import Money, Currency
from domain.repositories import ClientRepository

class TopUpWallet:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    def execute(self, client_id: str, amount: float, currency: str) -> None:
        client = self.client_repo.get(client_id)
        if not client:
            raise ValueError('Client not found')
        money = Money(amount=amount, currency=Currency(currency))
        client.wallet.deposit(money)
        self.client_repo.add(client)
