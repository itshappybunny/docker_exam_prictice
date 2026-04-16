Вот пошаговый план реализации в твоей Ubuntu.

### Шаг 1: Подготовка папки
Создай новую директорию, чтобы не смешивать с предыдущим заданием:
```bash
mkdir demand-forecast && cd demand-forecast
touch docker-compose.yml app.py requirements.txt
```

---

### Шаг 2: Написание Python-приложения (`app.py`)
Этот код создаст таблицу, позволит записывать данные о спросе и вычислять среднее по категориям.

```python
from flask import Flask, request, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

# Параметры подключения к PostgreSQL (из docker-compose)
DB_CONFIG = {
    "host": "db",
    "database": "forecast_db",
    "user": "admin",
    "password": "password"
}

def get_db_connection():
    # Ждем, пока база данных поднимется
    while True:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except:
            print("Ожидание базы данных...")
            time.sleep(2)

# Инициализация таблицы
conn = get_db_connection()
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS demand (
        id SERIAL PRIMARY KEY,
        category VARCHAR(50),
        item_name VARCHAR(50),
        quantity INTEGER
    );
''')
conn.commit()
cur.close()
conn.close()

@app.route('/add_demand', methods=['POST'])
def add_demand():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO demand (category, item_name, quantity) VALUES (%s, %s, %s)",
        (data['category'], data['item_name'], data['quantity'])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "Данные записаны"}), 201

# РАСШИРЕННАЯ ФУНКЦИОНАЛЬНОСТЬ: Средний спрос по категориям
@app.route('/average_demand', methods=['GET'])
def average_demand():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT category, AVG(quantity) FROM demand GROUP BY category")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    report = {row[0]: float(row[1]) for row in rows}
    return jsonify(report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

### Шаг 3: Зависимости (`requirements.txt`)
Впиши туда две библиотеки:
```text
flask
psycopg2-binary
```

---

### Шаг 4: Настройка `docker-compose.yml`
Здесь мы связываем Python и PostgreSQL.

```yaml
version: '3.8'

services:
  app:
    image: python:3.9-slim
    working_dir: /app
    volumes:
      - .:/app
    ports:
      - "5000:5000"
    command: sh -c "pip install -r requirements.txt && python app.py"
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: forecast_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

### Шаг 5: Запуск и проверка

1.  **Запусти сборку:**
    ```bash
    sudo docker-compose up -d
    ```
    *Подожди около минуты, пока скачается образ Postgres и установятся библиотеки Python.*

2.  **Проверь логи**, чтобы убедиться, что база готова: `sudo docker-compose logs -f app`.

3.  **Добавь данные (запиши в базу):**
    Выполни пару запросов в терминале:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"category": "Electronics", "item_name": "Phone", "quantity": 10}' http://localhost:5000/add_demand
    
    curl -X POST -H "Content-Type: application/json" -d '{"category": "Electronics", "item_name": "Laptop", "quantity": 20}' http://localhost:5000/add_demand
    
    curl -X POST -H "Content-Type: application/json" -d '{"category": "Food", "item_name": "Apple", "quantity": 50}' http://localhost:5000/add_demand
    ```

4.  **Проверь расчет среднего спроса:**
    ```bash
    curl http://localhost:5000/average_demand
    ```
    *Ожидаемый ответ: `{"Electronics": 15.0, "Food": 50.0}`.*

---

### Для защиты (почему это правильное решение):
1.  **Стек:** Использован Python Flask (легкий веб-фреймворк) и PostgreSQL (надежная реляционная БД).
2.  **Связь:** Контейнеры общаются по сети внутри Docker. Flask использует хост `db` для доступа к Postgres.
3.  **Аналитика:** Расчет среднего спроса реализован на стороне БД через SQL-запрос `AVG(quantity)` с группировкой по категориям (`GROUP BY category`). Это работает быстрее, чем если бы мы считали это в самом Python.
4.  **Стойкость:** Благодаря `volumes`, база данных сохранит все записи даже после полной остановки контейнеров.



sudo docker-compose up -d

curl -X POST -H "Content-Type: application/json" -d '{"category": "Electronics", "item_name": "Phone", "quantity": 10}' http://localhost:5000/add_demand

curl -X POST -H "Content-Type: application/json" -d '{"category": "Electronics", "item_name": "Laptop", "quantity": 20}' http://localhost:5000/add_demand

curl -X POST -H "Content-Type: application/json" -d '{"category": "Food", "item_name": "Apple", "quantity": 50}' http://localhost:5000/add_demand


curl http://localhost:5000/average_demand

*sudo docker compose up -d --build
