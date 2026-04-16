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