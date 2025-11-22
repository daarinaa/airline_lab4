## Установка и запуск

1. Установите зависимости:
```bash
python -m pip install -r requirements.txt

```

2. Создайте таблицы и наполните базу тестовыми данными:
```bash
python main.py

```

3. Запустите FastAPI приложение:
```bash
python app.py

```

4. Откройте в браузере документацию API: http://localhost:8000/docs

## Примеры использования API

### Создание пассажира
```bash
curl -X POST "http://localhost:8000/passengers/?full_name=Иванов%20Иван&passport_data=1234567890&contact_info=ivanov@mail.ru"

```

## Получение всех рейсов
```bash
curl -X GET "http://localhost:8000/flights/"

```

## Поиск доступных мест
```bash
curl -X GET "http://localhost:8000/flights/1/available-seats"

```
