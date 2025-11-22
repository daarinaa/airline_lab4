import requests

BASE_URL = "http://localhost:8000"

# Пример создания пассажира
def create_passenger_example():
    response = requests.post(
        f"{BASE_URL}/passengers/",
        params={
            "full_name": "Сидоров Петр",
            "passport_data": "1122334455", 
            "contact_info": "sidorov@mail.ru"
        }
    )
    print(response.json())

# Пример поиска рейсов по статусу
def find_flights_example():
    response = requests.get(f"{BASE_URL}/flights/status/scheduled")
    print(response.json())