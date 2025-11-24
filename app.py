from fastapi import FastAPI, HTTPException, status
from typing import List
import uvicorn

from database import engine
from models import *
from airline_requests import AirlineRequests

app = FastAPI()

requests = AirlineRequests()

@app.get("/passengers/", response_model=List[Passenger])
def get_passengers():
    return requests.get_all_passengers()

@app.get("/passengers/{passenger_id}", response_model=Passenger)
def get_passenger(passenger_id: int):
    passenger = requests.get_passenger_by_id(passenger_id)
    if not passenger:
        raise HTTPException(status_code=404, detail="Пассажир не найден")
    return passenger

@app.get("/flights/", response_model=List[Flight])
def get_flights():
    return requests.get_all_flights()

@app.get("/flights/status/{status}", response_model=List[Flight])
def get_flights_by_status(status: str):
    return requests.get_flights_by_status(status)

@app.get("/tickets/passenger/{passenger_id}", response_model=List[Ticket])
def get_tickets_by_passenger(passenger_id: int):
    return requests.get_tickets_by_passenger(passenger_id)

@app.get("/tickets/flight/{flight_id}", response_model=List[Ticket])
def get_tickets_by_flight(flight_id: int):
    return requests.get_tickets_by_flight(flight_id)

@app.get("/crew/flight/{flight_id}", response_model=List[Crew])
def get_crew_by_flight(flight_id: int):
    return requests.get_crew_by_flight(flight_id)

@app.get("/passengers/{passenger_id}/full")
def get_passenger_full_info(passenger_id: int):
    result = requests.get_passenger_full_info(passenger_id)
    if not result:
        raise HTTPException(status_code=404, detail="Пассажир не найден")
    return result

@app.get("/flights/{flight_id}/available-seats", response_model=List[Seat])
def get_available_seats(flight_id: int):
    return requests.get_available_seats(flight_id)

@app.post("/passengers/", response_model=Passenger)
def create_passenger(full_name: str, passport_data: str, contact_info: str):
    try:
        if not full_name or not passport_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя и паспортные данные обязательны"
            )
        return requests.create_passenger(full_name, passport_data, contact_info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании пассажира: {str(e)}"
        )
        
@app.put("/passengers/{passenger_id}", response_model=Passenger)
def update_passenger(
    passenger_id: int,
    full_name: str = None,
    passport_data: str = None,
    contact_info: str = None,
    status: str = None
):
    updated_passenger = requests.update_passenger(
        passenger_id, full_name, passport_data, contact_info, status
    )
    if not updated_passenger:
        raise HTTPException(status_code=404, detail="Пассажир не найден")
    return updated_passenger

@app.delete("/passengers/{passenger_id}")
def delete_passenger(passenger_id: int):
    success = requests.delete_passenger(passenger_id)
    if not success:
        raise HTTPException(status_code=404, detail="Пассажир не найден")
    return {"message": "Пассажир удален"}

@app.post("/tickets/", response_model=Ticket)
def create_ticket(passenger_id: int, flight_id: int, seat_id: int, price: float):
    return requests.create_ticket(passenger_id, flight_id, seat_id, price)

@app.put("/tickets/{ticket_id}/status", response_model=Ticket)
def update_ticket_status(ticket_id: int, status: str):
    ticket = requests.update_ticket_status(ticket_id, status)
    if not ticket:
        raise HTTPException(status_code=404, detail="Билет не найден")
    return ticket

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    success = requests.delete_ticket(ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Билет не найден")
    return {"message": "Билет удален"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)