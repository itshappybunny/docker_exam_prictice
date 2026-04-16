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