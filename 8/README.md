sudo docker-compose up -d

curl -X POST -H "Content-Type: application/json" -d '{"category": "Electronics", "item_name": "Phone", "quantity": 10}' http://localhost:5000/add_demand

curl -X POST -H "Content-Type: application/json" -d '{"category": "Electronics", "item_name": "Laptop", "quantity": 20}' http://localhost:5000/add_demand

curl -X POST -H "Content-Type: application/json" -d '{"category": "Food", "item_name": "Apple", "quantity": 50}' http://localhost:5000/add_demand


curl http://localhost:5000/average_demand

*sudo docker compose up -d --build
