from sqlmodel import SQLModel, Field, Relationship
from typing import List
from datetime import datetime

class Passenger(SQLModel, table=True):
    __tablename__ = "passenger"
    __table_args__ = {"schema": "nigamatulina"}
    
    passenger_id: int = Field(primary_key=True)
    full_name: str = Field(default="")
    passport_data: str = Field(default="")
    contact_info: str = Field(default="")
    status: str = Field(default="")

class Airplane(SQLModel, table=True):
    __tablename__ = "airplane"
    __table_args__ = {"schema": "nigamatulina"}
    
    plane_id: int = Field(primary_key=True)
    registration_number: str = Field(default="")
    model: str = Field(default="")
    capacity: int = Field(default=0)
    status: str = Field(default="")

class Seat(SQLModel, table=True):
    __tablename__ = "seat"
    __table_args__ = {"schema": "nigamatulina"}
    
    seat_id: int = Field(primary_key=True)
    plane_id: int = Field(foreign_key="nigamatulina.airplane.plane_id")
    row_number: int = Field(default=0)
    seat_number: str = Field(default="")
    seat_class: str = Field(default="")
    status: str = Field(default="")

class Flight(SQLModel, table=True):
    __tablename__ = "flight"
    __table_args__ = {"schema": "nigamatulina"}
    
    flight_id: int = Field(primary_key=True)
    flight_number: str = Field(default="")
    departure_date: datetime = Field(default=datetime.now())
    arrival_date: datetime = Field(default=datetime.now())
    status: str = Field(default="")
    plane_id: int = Field(foreign_key="nigamatulina.airplane.plane_id")

class Crew(SQLModel, table=True):
    __tablename__ = "crew"
    __table_args__ = {"schema": "nigamatulina"}
    
    crew_id: int = Field(primary_key=True)
    full_name: str = Field(default="")
    position: str = Field(default="")
    status: str = Field(default="")

class Ticket(SQLModel, table=True):
    __tablename__ = "ticket"
    __table_args__ = {"schema": "nigamatulina"}
    
    ticket_id: int = Field(primary_key=True)
    ticket_number: str = Field(default="")
    status: str = Field(default="")
    passenger_id: int = Field(foreign_key="nigamatulina.passenger.passenger_id")
    flight_id: int = Field(foreign_key="nigamatulina.flight.flight_id")
    seat_id: int = Field(foreign_key="nigamatulina.seat.seat_id")
    price: float = Field(default=0.0)

class Transaction(SQLModel, table=True):
    __tablename__ = "transaction"
    __table_args__ = {"schema": "nigamatulina"}
    
    transaction_id: int = Field(primary_key=True)
    ticket_id: int = Field(foreign_key="nigamatulina.ticket.ticket_id")
    amount: float = Field(default=0.0)
    currency: str = Field(default="")
    status: str = Field(default="")
    transaction_date: datetime = Field(default=datetime.now())

class Baggage(SQLModel, table=True):
    __tablename__ = "baggage"
    __table_args__ = {"schema": "nigamatulina"}
    
    baggage_id: int = Field(primary_key=True)
    ticket_id: int = Field(foreign_key="nigamatulina.ticket.ticket_id")
    weight: float = Field(default=0.0)
    baggage_type: str = Field(default="")
    status: str = Field(default="")

class Checkin(SQLModel, table=True):
    __tablename__ = "checkin"
    __table_args__ = {"schema": "nigamatulina"}
    
    checkin_id: int = Field(primary_key=True)
    ticket_id: int = Field(foreign_key="nigamatulina.ticket.ticket_id")
    baggage_checked: bool = Field(default=False)
    boarding_pass: str = Field(default="")
    status: str = Field(default="")

class CrewFlight(SQLModel, table=True):
    __tablename__ = "crewflight"
    __table_args__ = {"schema": "nigamatulina"}
    
    crew_id: int = Field(primary_key=True, foreign_key="nigamatulina.crew.crew_id")
    flight_id: int = Field(primary_key=True, foreign_key="nigamatulina.flight.flight_id")