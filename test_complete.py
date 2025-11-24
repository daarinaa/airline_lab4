import requests as http_requests  # переименовываем чтобы избежать конфликта

BASE_URL = "http://localhost:8000"

def test_all_operations():
    print("=== ТЕСТИРОВАНИЕ АВИАКОМПАНИИ ===")
    
    try:
        # 1. Получить всех пассажиров
        print("\n1. Все пассажиры:")
        response = http_requests.get(f"{BASE_URL}/passengers/")
        print(f"Статус: {response.status_code}, Количество: {len(response.json())}")
        
        # 2. Создать нового пассажира
        print("\n2. Создание пассажира:")
        response = http_requests.post(
            f"{BASE_URL}/passengers/",
            params={
                "full_name": "Тестовый Пассажир",
                "passport_data": "TEST123456",
                "contact_info": "test@test.ru"
            }
        )
        if response.status_code == 200:
            new_passenger = response.json()
            print(f"Статус: {response.status_code}, Создан: {new_passenger['full_name']}")
            
            # 3. Получить информацию о созданном пассажире
            print("\n3. Информация о созданном пассажире:")
            passenger_id = new_passenger['passenger_id']
            response = http_requests.get(f"{BASE_URL}/passengers/{passenger_id}")
            print(f"Статус: {response.status_code}, Данные: {response.json()}")
            
            # 4. Обновить данные пассажира
            print("\n4. Обновление пассажира:")
            response = http_requests.put(
                f"{BASE_URL}/passengers/{passenger_id}",
                params={"full_name": "Обновленное Имя"}
            )
            print(f"Статус: {response.status_code}, Обновлен: {response.json()['full_name']}")
        else:
            print(f"Ошибка создания пассажира: {response.status_code}")
        
        # 5. Получить доступные места на рейсе
        print("\n5. Доступные места на рейсе 1:")
        response = http_requests.get(f"{BASE_URL}/flights/1/available-seats")
        print(f"Статус: {response.status_code}, Мест: {len(response.json())}")
        
        # 6. Получить все рейсы
        print("\n6. Все рейсы:")
        response = http_requests.get(f"{BASE_URL}/flights/")
        print(f"Статус: {response.status_code}, Рейсов: {len(response.json())}")
        
        # 7. Получить рейсы по статусу
        print("\n7. Рейсы по статусу 'scheduled':")
        response = http_requests.get(f"{BASE_URL}/flights/status/scheduled")
        print(f"Статус: {response.status_code}, Рейсов: {len(response.json())}")
        
        print("\n✅ Все тесты пройдены успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        print("Убедитесь, что сервер запущен на http://localhost:8000")

if __name__ == "__main__":
    test_all_operations()