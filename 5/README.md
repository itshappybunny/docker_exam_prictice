Будем использовать язык запросов **Cypher**.

---

### Шаг 1: Подготовка папки
```bash
mkdir social-analyzer && cd social-analyzer
touch docker-compose.yml app.py requirements.txt
```

---

### Шаг 2: Написание Python-приложения (`app.py`)
Этот код будет создавать узлы пользователей и хештегов, а также искать самые популярные из них.

```python
from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import os

app = Flask(__name__)

# Настройки подключения к Neo4j
uri = "bolt://db:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def add_post_tx(tx, username, hashtag):
    # Создаем пользователя, хештег и связь между ними "USED"
    tx.run("MERGE (u:User {name: $username}) "
           "MERGE (h:Hashtag {name: $hashtag}) "
           "MERGE (u)-[:USED]->(h)", username=username, hashtag=hashtag)

@app.route('/add_post', methods=['POST'])
def add_post():
    data = request.json
    with driver.session() as session:
        session.execute_write(add_post_tx, data['username'], data['hashtag'])
    return jsonify({"status": "Пост зафиксирован"}), 201

# АНАЛИЗ: Популярность хештегов (графовый запрос)
@app.route('/popular_hashtags', methods=['GET'])
def get_popular():
    query = """
    MATCH (h:Hashtag)<-[:USED]-(u:User)
    RETURN h.name AS hashtag, count(u) AS usage_count
    ORDER BY usage_count DESC
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query)
        analysis = [{"hashtag": record["hashtag"], "count": record["usage_count"]} for record in result]
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

### Шаг 3: Зависимости (`requirements.txt`)
```text
flask
neo4j
```

---

### Шаг 4: Настройка `docker-compose.yml`
Neo4j требует чуть больше настроек (нужно принять лицензионное соглашение и задать пароль).

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
      db:
        condition: service_healthy

  db:
    image: neo4j:latest
    environment:
      NEO4J_AUTH: neo4j/password
      NEO4J_PLUGINS: '["apoc"]'
    ports:
      - "7474:7474" # Веб-интерфейс
      - "7687:7687" # Bolt протокол
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "password", "RETURN 1"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - neo4j_data:/data

volumes:
  neo4j_data:
```

---

### Шаг 5: Проверка работы

1.  **Запуск:**
    ```bash
    sudo docker-compose up -d
    ```
    *Neo4j тяжелая, дай ей минуту, чтобы запуститься.*

2.  **Добавь данные (имитация постов):**
    ```bash
    # Пользователь anna использует хештег #docker
    curl -X POST -H "Content-Type: application/json" -d '{"username": "anna", "hashtag": "docker"}' http://localhost:5000/add_post
    
    # Пользователь boris тоже использует #docker
    curl -X POST -H "Content-Type: application/json" -d '{"username": "boris", "hashtag": "docker"}' http://localhost:5000/add_post
    
    # Пользователь anna использует #python
    curl -X POST -H "Content-Type: application/json" -d '{"username": "anna", "hashtag": "python"}' http://localhost:5000/add_post
    ```

3.  **Проверь анализ популярности:**
    ```bash
    curl http://localhost:5000/popular_hashtags
    ```
    *Ответ должен показать, что `docker` популярнее (2 упоминания), чем `python` (1 упоминание).*

---

### Почему это крутое решение для билета:
1.  **Специфика:** Ты показала понимание **графовых баз данных**. Вместо таблиц ты работаешь с узлами (`User`, `Hashtag`) и связями (`USED`).
2.  **Язык Cypher:** В коде используется `MATCH` и `count(u)`, что является стандартом для Neo4j.
3.  **Визуализация:** Бонус для экзаменатора — скажи, что он может зайти в браузере на `http://localhost:7474` (логин/пароль: neo4j/password) и увидеть граф **визуально**. Это всегда производит впечатление «вау».
4.  **Healthcheck:** Мы используем проверку готовности базы через `cypher-shell`, что гарантирует стабильный запуск.

