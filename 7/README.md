Этот билет чуть сложнее предыдущих из-за **MySQL**. В отличие от MongoDB или Postgres, MySQL более требовательна к инициализации (нужно создать базу данных и таблицы при старте). Но не переживай, мы всё настроим так, чтобы оно взлетело с одной команды.

Вот план реализации для Node.js + MySQL.

---

### Шаг 1: Подготовка папки
Создаем рабочее пространство:
```bash
mkdir chat-bot && cd chat-bot
touch docker-compose.yml server.js package.json init.sql
```

---

### Шаг 2: Настройка базы данных (`init.sql`)
Чтобы при запуске MySQL сразу создала нужную таблицу, мы подготовим SQL-скрипт.
```sql
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Шаг 3: Написание кода чат-бота (`server.js`)
Этот сервер будет сохранять сообщения и анализировать частоту обращений.

```javascript
const express = require('express');
const mysql = require('mysql2/promise');
const app = express();
app.use(express.json());

const dbConfig = {
    host: 'db',
    user: 'user',
    password: 'password',
    database: 'chat_db'
};

// Маршрут для сохранения сообщения (логирование)
app.post('/message', async (req, res) => {
    try {
        const { customer_id, message } = req.body;
        const connection = await mysql.createConnection(dbConfig);
        await connection.execute(
            'INSERT INTO messages (customer_id, message) VALUES (?, ?)',
            [customer_id, message]
        );
        console.log(`[LOG]: Сообщение от клиента ${customer_id} сохранено.`);
        await connection.end();
        res.status(201).send({ status: "Сообщение получено" });
    } catch (err) {
        console.error(err);
        res.status(500).send("Ошибка базы данных");
    }
});

// РАСШИРЕННАЯ ФУНКЦИОНАЛЬНОСТЬ: Анализ частоты обращений
app.get('/analytics/frequency', async (req, res) => {
    try {
        const connection = await mysql.createConnection(dbConfig);
        // Считаем количество сообщений для каждого клиента
        const [rows] = await connection.execute(
            'SELECT customer_id, COUNT(*) as message_count FROM messages GROUP BY customer_id ORDER BY message_count DESC'
        );
        await connection.end();
        res.json(rows);
    } catch (err) {
        res.status(500).send("Ошибка при анализе");
    }
});

app.listen(3000, () => console.log('Chat-bot server is running on port 3000'));
```

---

### Шаг 4: Зависимости (`package.json`)
```json
{
  "name": "chat-bot",
  "version": "1.0.0",
  "main": "server.js",
  "dependencies": {
    "express": "^4.18.2",
    "mysql2": "^3.0.0"
  }
}
```

---

### Шаг 5: Конфигурация Docker Compose (`docker-compose.yml`)
Тут важно пробросить `init.sql` в специальную папку MySQL, чтобы она выполнила его при первом запуске.

```yaml
version: '3.8'

services:
  app:
    image: node:18
    working_dir: /usr/src/app
    volumes:
      - .:/usr/src/app
    ports:
      - "3000:3000"
    command: sh -c "npm install && node server.js"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: chat_db
      MYSQL_USER: user
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "user", "-ppassword"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mysql_data:
```

---

### Шаг 6: Запуск и проверка

1.  **Запуск:**
    ```bash
    sudo docker-compose up -d
    ```

2.  **Проверка логирования:**
    Отправь пару сообщений от разных клиентов (имитируем работу бота):
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"customer_id": 101, "message": "Hello!"}' http://localhost:3000/message
    curl -X POST -H "Content-Type: application/json" -d '{"customer_id": 102, "message": "Need help"}' http://localhost:3000/message
    curl -X POST -H "Content-Type: application/json" -d '{"customer_id": 101, "message": "Are you there?"}' http://localhost:3000/message
    ```

3.  **Проверка логов в терминале:**
    ```bash
    sudo docker-compose logs app
    ```
    *(Ты должна увидеть строки: `[LOG]: Сообщение от клиента 101 сохранено.`)*

4.  **Анализ частоты:**
    ```bash
    curl http://localhost:3000/analytics/frequency
    ```
    *Ответ покажет, что клиент 101 писал 2 раза, а 102 — один раз.*

---

### Почему это решение «на отлично»:
* **Инициализация БД:** Ты не просто создала пустую базу, а использовала `docker-entrypoint-initdb.d` — это профессиональный способ разворачивать структуру таблиц в Docker.
* **Healthcheck:** В `docker-compose` добавлена проверка здоровья базы. Node.js не начнет запускаться, пока MySQL не подтвердит, что она готова принимать соединения. Это решает проблему падения приложения при старте.
* **Аналитика:** SQL-запрос с `COUNT` и `GROUP BY` — это эталонный способ анализа частоты событий в реляционных базах.
