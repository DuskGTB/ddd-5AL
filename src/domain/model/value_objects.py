from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, EmailStr, validator
import uuid

class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    JPY = "JPY"
    CHF = "CHF"

class Money(BaseModel):
    amount: float
    currency: Currency = Currency.EUR

    @validator('amount')
    def amount_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Amount must be non-negative')
        return v

    def to_eur(self) -> Money:
        rates = {
            Currency.EUR: 1.0,
            Currency.USD: 0.91,
            Currency.GBP: 1.17,
            Currency.JPY: 0.0068,
            Currency.CHF: 1.02,
        }
        rate = rates[self.currency]
        return Money(amount=self.amount * rate, currency=Currency.EUR)

    def __add__(self, other: Money) -> Money:
        if self.currency != Currency.EUR:
            return self.to_eur() + other
        if other.currency != Currency.EUR:
            return self + other.to_eur()
        return Money(amount=self.amount + other.amount, currency=Currency.EUR)

    def __mul__(self, factor: float) -> Money:
        return Money(amount=self.amount * factor, currency=self.currency)

class PhoneNumber(BaseModel):
    number: str

    @validator('number')
    def valid_phone(cls, v):
        digits = ''.join(filter(str.isdigit, v))
        if len(digits) < 8 or len(digits) > 15:
            raise ValueError('Phone number must have between 8 and 15 digits')
        return v

class ClientId(str):
    @classmethod
    def new(cls) -> ClientId:
        return cls(str(uuid.uuid4()))

class ReservationId(str):
    @classmethod
    def new(cls) -> ReservationId:
        return cls(str(uuid.uuid4()))
