from pydantic import BaseModel
from .value_objects import Money

class Wallet(BaseModel):
    balance: Money = Money(amount=0)

    def deposit(self, money: Money) -> None:
        eur = money.to_eur()
        self.balance = Money(amount=self.balance.amount + eur.amount, currency=eur.currency)

    def debit(self, money: Money) -> None:
        eur = money.to_eur()
        if self.balance.amount < eur.amount:
            raise ValueError('Insufficient funds')
        self.balance = Money(amount=self.balance.amount - eur.amount, currency=eur.currency)
