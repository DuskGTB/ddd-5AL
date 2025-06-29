from pydantic import BaseModel, EmailStr
from pydantic.config import ConfigDict
from .value_objects import ClientId, PhoneNumber
from .wallet import Wallet

class Client(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: ClientId
    name: str
    email: EmailStr
    phone: PhoneNumber
    wallet: Wallet