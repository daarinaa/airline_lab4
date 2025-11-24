from sqlmodel import Session, select
from database import engine
from models import *
from typing import List, Optional
from datetime import datetime

class AirlineRequests:
    def get_all_passengers(self) -> List[Passenger]:
        with Session(engine) as session:
            statement = select(Passenger)
            results = session.exec(statement)
            return results.all()
    
    def get_passenger_by_id(self, passenger_id: int) -> Passenger:
        with Session(engine) as session:
            return session.get(Passenger, passenger_id)
    
    def get_all_flights(self) -> List[Flight]:
        with Session(engine) as session:
            statement = select(Flight)
            results = session.exec(statement)
            return results.all()
    
    def get_flights_by_status(self, status: str) -> List[Flight]:
        with Session(engine) as session:
            statement = select(Flight).where(Flight.status == status)
            results = session.exec(statement)
            return results.all()
    
    def get_available_seats(self, flight_id: int) -> List[Seat]:
        with Session(engine) as session:
            flight = session.get(Flight, flight_id)
            if not flight:
                return []
            statement = select(Seat).where(Seat.plane_id == flight.plane_id, Seat.status == "free")
            results = session.exec(statement)
            return results.all()
    
    def get_tickets_by_passenger(self, passenger_id: int) -> List[Ticket]:
        with Session(engine) as session:
            statement = select(Ticket).where(Ticket.passenger_id == passenger_id)
            results = session.exec(statement)
            return results.all()
    
    def get_tickets_by_flight(self, flight_id: int) -> List[Ticket]:
        with Session(engine) as session:
            statement = select(Ticket).where(Ticket.flight_id == flight_id)
            results = session.exec(statement)
            return results.all()
    
    def get_transactions_by_ticket(self, ticket_id: int) -> List[Transaction]:
        with Session(engine) as session:
            statement = select(Transaction).where(Transaction.ticket_id == ticket_id)
            results = session.exec(statement)
            return results.all()
    
    def get_baggage_by_ticket(self, ticket_id: int) -> List[Baggage]:
        with Session(engine) as session:
            statement = select(Baggage).where(Baggage.ticket_id == ticket_id)
            results = session.exec(statement)
            return results.all()
    
    def get_checkin_by_ticket(self, ticket_id: int) -> Checkin:
        with Session(engine) as session:
            statement = select(Checkin).where(Checkin.ticket_id == ticket_id)
            results = session.exec(statement)
            return results.first()
    
    def get_crew_by_flight(self, flight_id: int) -> List[Crew]:
        with Session(engine) as session:
            statement = select(Crew).join(CrewFlight).where(CrewFlight.flight_id == flight_id)
            results = session.exec(statement)
            return results.all()
    
    def get_passenger_full_info(self, passenger_id: int):
        with Session(engine) as session:
            passenger = session.get(Passenger, passenger_id)
            if passenger:
                tickets = self.get_tickets_by_passenger(passenger_id)
                result = {"passenger": passenger, "tickets": []}
                for ticket in tickets:
                    flight = session.get(Flight, ticket.flight_id)
                    seat = session.get(Seat, ticket.seat_id)
                    transactions = self.get_transactions_by_ticket(ticket.ticket_id)
                    baggage = self.get_baggage_by_ticket(ticket.ticket_id)
                    checkin = self.get_checkin_by_ticket(ticket.ticket_id)
                    result["tickets"].append({
                        "ticket": ticket,
                        "flight": flight,
                        "seat": seat,
                        "transactions": transactions,
                        "baggage": baggage,
                        "checkin": checkin
                    })
                return result
            return None

    def create_passenger(self, full_name: str, passport_data: str, contact_info: str) -> Passenger:
        with Session(engine) as session:
            max_id = session.exec(select(Passenger.passenger_id)).all()
            next_id = max(max_id) + 1 if max_id else 1
            
            passenger = Passenger(
                passenger_id=next_id,
                full_name=full_name,
                passport_data=passport_data,
                contact_info=contact_info,
                status="active"
            )
            session.add(passenger)
            session.commit()
            session.refresh(passenger)
            return passenger
    
    def update_passenger(self, passenger_id: int, full_name: str = None, passport_data: str = None, 
                        contact_info: str = None, status: str = None) -> Optional[Passenger]:
        with Session(engine) as session:
            passenger = session.get(Passenger, passenger_id)
            if passenger:
                if full_name is not None:
                    passenger.full_name = full_name
                if passport_data is not None:
                    passenger.passport_data = passport_data
                if contact_info is not None:
                    passenger.contact_info = contact_info
                if status is not None:
                    passenger.status = status
                
                session.add(passenger)
                session.commit()
                session.refresh(passenger)
                return passenger
            return None
    
    def delete_passenger(self, passenger_id: int) -> bool:
        with Session(engine) as session:
            passenger = session.get(Passenger, passenger_id)
            if passenger:
                session.delete(passenger)
                session.commit()
                return True
            return False
    
    def create_ticket(self, passenger_id: int, flight_id: int, seat_id: int, price: float) -> Ticket:
        with Session(engine) as session:
            max_id = session.exec(select(Ticket.ticket_id)).all()
            next_id = max(max_id) + 1 if max_id else 1
            
            ticket = Ticket(
                ticket_id=next_id,
                ticket_number=f"TK{passenger_id:06d}{flight_id:04d}",
                status="booked",
                passenger_id=passenger_id,
                flight_id=flight_id,
                seat_id=seat_id,
                price=price
            )
            session.add(ticket)
            session.commit()
            session.refresh(ticket)
            return ticket
    
    def update_ticket_status(self, ticket_id: int, status: str) -> Optional[Ticket]:
        with Session(engine) as session:
            ticket = session.get(Ticket, ticket_id)
            if ticket:
                ticket.status = status
                session.add(ticket)
                session.commit()
                session.refresh(ticket)
                return ticket
            return None
    
    def delete_ticket(self, ticket_id: int) -> bool:
        with Session(engine) as session:
            ticket = session.get(Ticket, ticket_id)
            if ticket:
                session.delete(ticket)
                session.commit()
                return True
            return False

if __name__ == "__main__":
    requests = AirlineRequests()
    
    print("Все пассажиры:")
    passengers = requests.get_all_passengers()
    for p in passengers:
        print(f"{p.passenger_id}: {p.full_name}")
    
    print("\nВсе рейсы:")
    flights = requests.get_all_flights()
    for f in flights:
        print(f"{f.flight_id}: {f.flight_number} - {f.status}")
    
    print("\nЭкипаж рейса 1:")
    crew = requests.get_crew_by_flight(1)
    for c in crew:
        print(f"{c.full_name} - {c.position}")
    
    print("\nПолная информация о пассажире 1:")
    passenger_info = requests.get_passenger_full_info(1)
    if passenger_info:
        print(f"Пассажир: {passenger_info['passenger'].full_name}")
        print(f"Билеты: {len(passenger_info['tickets'])}")