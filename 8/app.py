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