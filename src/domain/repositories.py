from __future__ import annotations
from abc import ABC, abstractmethod
from .model.client import Client
from .model.reservation import Reservation
from .model.value_objects import ClientId, ReservationId
from typing import Optional

class ClientRepository(ABC):
    @abstractmethod
    def add(self, client: Client) -> None:
        ...

    @abstractmethod
    def get(self, client_id: ClientId) -> Optional[Client]:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Client]:
        ...

class ReservationRepository(ABC):
    @abstractmethod
    def add(self, reservation: Reservation) -> None:
        ...

    @abstractmethod
    def get(self, reservation_id: ReservationId) -> Optional[Reservation]:
        ...

    @abstractmethod
    def update(self, reservation: Reservation) -> None:
        ...