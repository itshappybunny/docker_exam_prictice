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