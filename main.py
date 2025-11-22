from database import create_schema_and_tables, engine
from models import *
from sqlmodel import Session, select
from datetime import datetime

def create_sample_data():
    with Session(engine) as session:
        existing = session.exec(select(Passenger)).first()
        if existing:
            print("Данные уже существуют")
            return

        print("Создание тестовых данных...")
        
        passenger1 = Passenger(passenger_id=1, full_name="Иванов Иван", passport_data="1234567890", contact_info="ivanov@mail.ru", status="active")
        passenger2 = Passenger(passenger_id=2, full_name="Петрова Мария", passport_data="0987654321", contact_info="petrova@mail.ru", status="active")
        session.add_all([passenger1, passenger2])
        session.flush()

        airplane1 = Airplane(plane_id=1, registration_number="RA-73851", model="Boeing 737", capacity=189, status="ready")
        airplane2 = Airplane(plane_id=2, registration_number="VP-BRS", model="Airbus A320", capacity=180, status="ready")
        session.add_all([airplane1, airplane2])
        session.flush()

        seat1 = Seat(seat_id=1, plane_id=1, row_number=1, seat_number="1A", seat_class="business", status="free")
        seat2 = Seat(seat_id=2, plane_id=1, row_number=1, seat_number="1B", seat_class="business", status="free")
        seat3 = Seat(seat_id=3, plane_id=2, row_number=10, seat_number="10C", seat_class="economy", status="free")
        session.add_all([seat1, seat2, seat3])
        session.flush()

        flight1 = Flight(flight_id=1, flight_number="SU-1234", departure_date=datetime(2024, 2, 20, 10, 0, 0), arrival_date=datetime(2024, 2, 20, 12, 0, 0), status="scheduled", plane_id=1)
        flight2 = Flight(flight_id=2, flight_number="SU-5678", departure_date=datetime(2024, 2, 21, 14, 0, 0), arrival_date=datetime(2024, 2, 21, 17, 0, 0), status="scheduled", plane_id=2)
        session.add_all([flight1, flight2])
        session.flush()

        ticket1 = Ticket(ticket_id=1, ticket_number="TK001234", status="confirmed", passenger_id=1, flight_id=1, seat_id=1, price=12000.00)
        ticket2 = Ticket(ticket_id=2, ticket_number="TK005678", status="confirmed", passenger_id=2, flight_id=2, seat_id=3, price=15000.00)
        session.add_all([ticket1, ticket2])
        session.flush()

        transaction1 = Transaction(transaction_id=1, ticket_id=1, amount=12000.00, currency="RUB", status="success", transaction_date=datetime.now())
        transaction2 = Transaction(transaction_id=2, ticket_id=2, amount=15000.00, currency="RUB", status="success", transaction_date=datetime.now())
        session.add_all([transaction1, transaction2])
        session.flush()

        baggage1 = Baggage(baggage_id=1, ticket_id=1, weight=23.5, baggage_type="checked", status="checked")
        baggage2 = Baggage(baggage_id=2, ticket_id=2, weight=15.0, baggage_type="checked", status="checked")
        session.add_all([baggage1, baggage2])
        session.flush()

        checkin1 = Checkin(checkin_id=1, ticket_id=1, baggage_checked=True, boarding_pass="BP001234", status="completed")
        checkin2 = Checkin(checkin_id=2, ticket_id=2, baggage_checked=True, boarding_pass="BP005678", status="completed")
        session.add_all([checkin1, checkin2])
        session.flush()

        crew1 = Crew(crew_id=1, full_name="Сидоров Алексей", position="pilot", status="active")
        crew2 = Crew(crew_id=2, full_name="Козлова Анна", position="stewardess", status="active")
        session.add_all([crew1, crew2])
        session.flush()

        crew_flight1 = CrewFlight(crew_id=1, flight_id=1)
        crew_flight2 = CrewFlight(crew_id=2, flight_id=1)
        session.add_all([crew_flight1, crew_flight2])

        session.commit()
        print("Тестовые данные созданы!")

if __name__ == "__main__":
    create_schema_and_tables()
    create_sample_data()