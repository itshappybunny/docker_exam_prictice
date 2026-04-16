Вот пошаговый план реализации:

---

## Шаг 1: Подготовка структуры проекта
Создай рабочую директорию и файлы приложения:

```bash
mkdir sales-analytics && cd sales-analytics
touch docker-compose.yml server.js package.json
```

---

## Шаг 2: Создание Node.js приложения (`server.js`)
Нам нужно написать простой сервер, который умеет подключаться к MongoDB, сохранять данные о продажах и выдавать отчет по выручке.

**Отредактируй `server.js`:**
```javascript
const express = require('express');
const mongoose = require('mongoose');
const app = express();
app.use(express.json());

// Подключение к MongoDB (используем имя сервиса из docker-compose)
mongoose.connect('mongodb://db:27017/salesdb', { useNewUrlParser: true, useUnifiedTopology: true });

const Sale = mongoose.model('Sale', {
    item: String,
    price: Number,
    date: Date
});

// Маршрут для добавления продажи
app.post('/sales', async (req, res) => {
    const sale = new Sale(req.body);
    await sale.save();
    res.send({ message: "Продажа сохранена!" });
});

// НОВАЯ ФУНКЦИОНАЛЬНОСТЬ: Отчет по выручке за месяц
app.get('/report/revenue', async (req, res) => {
    const now = new Date();
    const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
    
    const stats = await Sale.aggregate([
        { $match: { date: { $gte: firstDay } } },
        { $group: { _id: null, totalRevenue: { $sum: "$price" } } }
    ]);
    
    const revenue = stats.length > 0 ? stats[0].totalRevenue : 0;
    res.json({ month: now.toLocaleString('default', { month: 'long' }), totalRevenue: revenue });
});

app.listen(3000, () => console.log('Server is running on port 3000'));
```

---

## Шаг 3: Настройка окружения (`package.json`)
Файл нужен для установки зависимостей внутри контейнера.

**Отредактируй `package.json`:**
```json
{
  "name": "sales-analytics",
  "version": "1.0.0",
  "main": "server.js",
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.0.0"
  }
}
```

---

## Шаг 4: Создание `docker-compose.yml`
Это сердце нашего задания. Мы свяжем Node.js и MongoDB в одну сеть.

**Отредактируй `docker-compose.yml`:**
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
      - db

  db:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

---

## Шаг 5: Запуск и проверка

1.  **Запусти приложение:**
    ```bash
    sudo docker-compose up -d
    ```
    *Эта команда скачает образы, создаст сеть и запустит оба контейнера.*

2.  **Проверь статус:** `sudo docker-compose ps`. Должно быть написано `Up`.

3.  **Проверь взаимодействие (API):**
    Используем `curl` прямо в терминале Ubuntu, чтобы добавить тестовую продажу:
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"item": "Laptop", "price": 1000, "date": "2026-04-10"}' \
    http://localhost:3000/sales
    ```

4.  **Проверь аналитический отчет:**
    ```bash
    curl http://localhost:3000/report/revenue
    ```
    *В ответе ты должен увидеть сумму всех продаж за текущий месяц.*

---

## Как это работает (для защиты билета):
1.  **Многоконтейнерность:** Мы разделили логику (Node.js) и данные (MongoDB). Они общаются по внутренней сети Docker по имени сервиса `db`.
2.  **Volumes:** В Docker Compose мы прописали `mongodb_data`, чтобы при перезагрузке контейнера данные о продажах не удалялись.
3.  **Агрегация:** Для отчета мы использовали `$group` и `$sum` в MongoDB — это эффективный способ считать финансовые показатели.



sudo docker-compose up -d

curl -X POST -H "Content-Type: application/json" \
-d '{"item": "Laptop", "price": 1000, "date": "2026-04-10"}' \
http://localhost:3000/sales

curl http://localhost:3000/report/revenue
