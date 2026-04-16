from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Подключение к MongoDB
client = MongoClient('mongodb://db:27017/')
db = client.finance_db
transactions = db.transactions

@app.route('/add_income', methods=['POST'])
def add_income():
    data = request.json
    # Сохраняем сумму и дату
    transactions.insert_one({
        "amount": float(data['amount']),
        "category": data.get('category', 'general'),
        "date": datetime.now()
    })
    return jsonify({"status": "Доход зафиксирован"}), 201

# АГРЕГАЦИЯ: Общая сумма доходов
@app.route('/total_income', methods=['GET'])
def get_total():
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]
    result = list(transactions.aggregate(pipeline))
    total = result[0]['total'] if result else 0
    return jsonify({"total_income": total})

# ПРОГНОЗ: Доход на следующий квартал
@app.route('/forecast', methods=['GET'])
def get_forecast():
    # Считаем средний доход в месяц на основе всех данных
    pipeline = [
        {"$group": {"_id": None, "avg_amount": {"$avg": "$amount"}, "count": {"$sum": 1}}}
    ]
    result = list(transactions.aggregate(pipeline))
    
    if not result:
        return jsonify({"forecast_next_quarter": 0, "message": "Нет данных для прогноза"})

    # Упрощенная логика: берем среднее значение транзакции и умножаем на 3 
    # (предполагая, что в квартале 3 месяца и в среднем 1 доходная операция в месяц)
    # Или просто: средний доход за всё время * 3
    avg_val = result[0]['avg_amount']
    forecast = round(avg_val * 3, 2)
    
    return jsonify({
        "period": "Next Quarter",
        "predicted_income": forecast,
        "basis": "Based on average transaction value"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)