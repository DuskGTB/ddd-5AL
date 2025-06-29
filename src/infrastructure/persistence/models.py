from sqlalchemy import Column, String, Float, Boolean, Date, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .database import engine

Base = declarative_base()

reservation_room = Table(
    'reservation_room', Base.metadata,
    Column('reservation_id', String, ForeignKey('reservations.id'), primary_key=True),
    Column('room_type',    String, ForeignKey('rooms.type'),       primary_key=True)
)

class ClientORM(Base):
    __tablename__ = 'clients'
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    balance = Column(Float, default=0.0)

class ReservationORM(Base):
    __tablename__ = 'reservations'
    id = Column(String, primary_key=True, index=True)
    client_id = Column(String, ForeignKey('clients.id'))
    checkin_date = Column(Date, nullable=False)
    nights = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    deposit_paid = Column(Boolean, default=False)
    confirmed = Column(Boolean, default=False)
    rooms = relationship('RoomORM', secondary=reservation_room)

class RoomORM(Base):
    __tablename__ = 'rooms'
    type = Column(String, primary_key=True)

Base.metadata.create_all(bind=engine)