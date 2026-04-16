sudo docker-compose up -d

curl -X POST -H "Content-Type: application/json" \
-d '{"item": "Laptop", "price": 1000, "date": "2026-04-10"}' \
http://localhost:3000/sales

curl http://localhost:3000/report/revenue
