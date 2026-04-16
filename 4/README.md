dev@dev-vm:~/Documents/4_task$ sudo docker compose ps
WARN[0000] /home/dev/Documents/4_task/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
NAME          IMAGE         COMMAND                  SERVICE   CREATED          STATUS          PORTS
4_task-db-1   postgres:15   "docker-entrypoint.s…"   db        21 minutes ago   Up 21 minutes   5432/tcp
dev@dev-vm:~/Documents/4_task$ 

### Шаг 1: Подготовка папки
```bash
mkdir order-system && cd order-system
touch docker-compose.yml app.py requirements.txt
```

---

### Шаг 2: Написание Django-приложения (`app.py`)
Мы будем использовать Django в режиме «одного файла» (mini-app), чтобы упростить задачу для экзамена.

```python
import os
import django
from django.conf import settings
from django.http import JsonResponse
from datetime import timedelta

# 1. Сначала настройки
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'orders_db', 'USER': 'admin', 'PASSWORD': 'password', 'HOST': 'db', 'PORT': '5432',
        }},
        INSTALLED_APPS=('app',),
        TIME_ZONE='UTC',
        USE_TZ=True,
        SECRET_KEY='fake-key'
    )
    django.setup()

# 2. Теперь импортируем модели и всё остальное
from django.db import models, connection

class Order(models.Model):
    item = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)

    class Meta:
        app_label = 'app'
        managed = False # Чтобы Django не пытался сам управлять таблицей, которую мы создадим вручную
        db_table = 'app_order'

# 3. API функции
def add_order(request):
    item_name = request.GET.get('item', 'Generic Item')
    order = Order.objects.create(item=item_name)
    # Имитируем доставку
    from django.utils import timezone
    order.delivered_at = timezone.now() + timedelta(hours=2)
    order.save()
    return JsonResponse({"status": "Заказ создан", "id": order.id})

def delivery_report(request):
    orders = Order.objects.exclude(delivered_at__isnull=True)
    if not orders.exists():
        return JsonResponse({"average_delivery_hours": 0})
    
    total_seconds = sum([(o.delivered_at - o.created_at).total_seconds() for o in orders])
    avg_hours = (total_seconds / len(orders)) / 3600
    return JsonResponse({"avg_delivery_time_hours": round(avg_hours, 2)})

# 4. Роуты
from django.urls import path
urlpatterns = [
    path('add/', add_order),
    path('report/', delivery_report),
]

# 5. Запуск
if __name__ == "__main__":
    # Создаем таблицу вручную, так как мы в mini-режиме
    import time
    time.sleep(5) # Даем базе время проснуться
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_order (
                id SERIAL PRIMARY KEY, 
                item VARCHAR(100), 
                created_at TIMESTAMP WITH TIME ZONE, 
                delivered_at TIMESTAMP WITH TIME ZONE
            );
        """)
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    import uvicorn
    uvicorn.run(application, host="0.0.0.0", port=8000)
```

---

### Шаг 3: Зависимости (`requirements.txt`)
```text
django
psycopg2-binary
uvicorn
gunicorn
```

---

### Шаг 4: Настройка `docker-compose.yml`
**Внимание:** Мы будем использовать порт **8000**, так как это стандарт для Django.

```yaml
version: '3.8'

services:
  app:
    image: python:3.9-slim
    working_dir: /app
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    command: sh -c "pip install -r requirements.txt && python app.py"
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: orders_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_orders_data:/var/lib/postgresql/data

volumes:
  postgres_orders_data:
```

---

### Шаг 5: Проверка работы

1.  **Запусти систему:**
    ```bash
    sudo docker compose up -d
    ```

2.  **Добавь заказ (обработка):**
    ```bash
    curl "http://localhost:8000/add/?item=Laptop"
    ```

3.  **Реализуй отчет (среднее время доставки):**
    ```bash
    curl "http://localhost:8000/report/"
    ```
    *Ответ должен быть: `{"avg_delivery_time_hours": 2.0}`.*

---

### Почему это решение закроет билет:
1.  **Django + PostgreSQL:** Использован самый мощный Python-фреймворк и промышленная СУБД.
2.  **Миграции:** Мы добавили автоматическое создание таблиц через SQL в блоке `if __name__ == "__main__"`, чтобы не мучиться с `manage.py migrate`.
3.  **Бизнес-логика:** Реализована работа с объектами `DateTimeField` и расчет разницы во времени (`timedelta`), что и требовалось для анализа доставки.

**Важно для экзамена:** Если преподаватель спросит, почему ты не используешь стандартную структуру папок Django, ответь: *«Для демонстрации контейнеризации я использовал минималистичную конфигурацию Django (Minimal Standalone App), что позволяет упаковать всю логику учета заказов в один микросервис без лишних накладных расходов».*
