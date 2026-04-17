dev@dev-vm:~/Documents/4_task_2$ docker compose up --build
[+] up 4/4
 ✔ Network 4_task_2_default             Created                                               0.1s
 ✔ Volume 4_task_2_postgres_orders_data Created                                               0.0s
 ✔ Container 4_task_2-db-1              Created                                               0.1s
 ✔ Container 4_task_2-app-1             Created                                               0.0s
Attaching to app-1, db-1
db-1  | The files belonging to this database system will be owned by user "postgres".
db-1  | This user must also own the server process.
db-1  | 
db-1  | The database cluster will be initialized with locale "en_US.utf8".
db-1  | The default database encoding has accordingly been set to "UTF8".
db-1  | The default text search configuration will be set to "english".
db-1  | 
db-1  | Data page checksums are disabled.
db-1  | 
db-1  | fixing permissions on existing directory /var/lib/postgresql/data ... ok
db-1  | creating subdirectories ... ok
db-1  | selecting dynamic shared memory implementation ... posix
db-1  | selecting default max_connections ... 100
db-1  | selecting default shared_buffers ... 128MB
db-1  | selecting default time zone ... Etc/UTC
db-1  | creating configuration files ... ok
db-1  | running bootstrap script ... ok
db-1  | performing post-bootstrap initialization ... ok
db-1  | initdb: warning: enabling "trust" authentication for local connections
db-1  | initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
db-1  | syncing data to disk ... ok
db-1  | 
db-1  | 
db-1  | Success. You can now start the database server using:
db-1  | 
db-1  |     pg_ctl -D /var/lib/postgresql/data -l logfile start
db-1  | 
db-1  | waiting for server to start....2026-04-17 00:23:15.578 UTC [47] LOG:  starting PostgreSQL 15.17 (Debian 15.17-1.pgdg13+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
db-1  | 2026-04-17 00:23:15.582 UTC [47] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db-1  | 2026-04-17 00:23:15.592 UTC [50] LOG:  database system was shut down at 2026-04-17 00:23:14 UTC
db-1  | 2026-04-17 00:23:15.603 UTC [47] LOG:  database system is ready to accept connections
db-1  |  done
db-1  | server started
db-1  | CREATE DATABASE
db-1  | 
db-1  | 
db-1  | /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
db-1  | 
db-1  | waiting for server to shut down....2026-04-17 00:23:15.853 UTC [47] LOG:  received fast shutdown request
db-1  | 2026-04-17 00:23:15.855 UTC [47] LOG:  aborting any active transactions
db-1  | 2026-04-17 00:23:15.866 UTC [47] LOG:  background worker "logical replication launcher" (PID 53) exited with exit code 1
db-1  | 2026-04-17 00:23:15.872 UTC [48] LOG:  shutting down
db-1  | 2026-04-17 00:23:15.874 UTC [48] LOG:  checkpoint starting: shutdown immediate
db-1  | 2026-04-17 00:23:16.104 UTC [48] LOG:  checkpoint complete: wrote 922 buffers (5.6%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.060 s, sync=0.163 s, total=0.233 s; sync files=301, longest=0.008 s, average=0.001 s; distance=4239 kB, estimate=4239 kB
db-1  | 2026-04-17 00:23:16.111 UTC [47] LOG:  database system is shut down
db-1  |  done
db-1  | server stopped
db-1  | 
db-1  | PostgreSQL init process complete; ready for start up.
db-1  | 
db-1  | 2026-04-17 00:23:16.196 UTC [1] LOG:  starting PostgreSQL 15.17 (Debian 15.17-1.pgdg13+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
db-1  | 2026-04-17 00:23:16.196 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db-1  | 2026-04-17 00:23:16.196 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db-1  | 2026-04-17 00:23:16.202 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db-1  | 2026-04-17 00:23:16.215 UTC [63] LOG:  database system was shut down at 2026-04-17 00:23:16 UTC
db-1  | 2026-04-17 00:23:16.221 UTC [1] LOG:  database system is ready to accept connections
app-1  | Collecting django
app-1  |   Downloading django-4.2.30-py3-none-any.whl (8.0 MB)
app-1  |      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.0/8.0 MB 10.0 MB/s eta 0:00:00
app-1  | Collecting psycopg2-binary
app-1  |   Downloading psycopg2_binary-2.9.11-cp39-cp39-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (4.2 MB)
app-1  |      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.2/4.2 MB 10.3 MB/s eta 0:00:00
app-1  | Collecting uvicorn
app-1  |   Downloading uvicorn-0.39.0-py3-none-any.whl (68 kB)
app-1  |      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 68.5/68.5 kB 11.8 MB/s eta 0:00:00
app-1  | Collecting gunicorn
app-1  |   Downloading gunicorn-23.0.0-py3-none-any.whl (85 kB)
app-1  |      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 85.0/85.0 kB 19.9 MB/s eta 0:00:00
app-1  | Collecting asgiref<4,>=3.6.0
app-1  |   Downloading asgiref-3.11.1-py3-none-any.whl (24 kB)
app-1  | Collecting sqlparse>=0.3.1
app-1  |   Downloading sqlparse-0.5.5-py3-none-any.whl (46 kB)
app-1  |      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 46.1/46.1 kB 10.3 MB/s eta 0:00:00
app-1  | Collecting click>=7.0
app-1  |   Downloading click-8.1.8-py3-none-any.whl (98 kB)
app-1  |      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 98.2/98.2 kB 14.5 MB/s eta 0:00:00
app-1  | Collecting h11>=0.8
app-1  |   Downloading h11-0.16.0-py3-none-any.whl (37 kB)
app-1  | Collecting typing-extensions>=4.0
app-1  |   Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
app-1  |      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.6/44.6 kB 7.1 MB/s eta 0:00:00
app-1  | Collecting packaging
app-1  |   Downloading packaging-26.1-py3-none-any.whl (95 kB)
app-1  |      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 95.8/95.8 kB 8.6 MB/s eta 0:00:00
app-1  | Installing collected packages: typing-extensions, sqlparse, psycopg2-binary, packaging, h11, click, uvicorn, gunicorn, asgiref, django
app-1  | Successfully installed asgiref-3.11.1 click-8.1.8 django-4.2.30 gunicorn-23.0.0 h11-0.16.0 packaging-26.1 psycopg2-binary-2.9.11 sqlparse-0.5.5 typing-extensions-4.15.0 uvicorn-0.39.0
app-1  | WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
app-1  | 
app-1  | [notice] A new release of pip is available: 23.0.1 -> 26.0.1
app-1  | [notice] To update, run: pip install --upgrade pip
app-1  |   File "/app/main.py", line 1
app-1  |     dev@dev-vm:~/Documents/4_task_2$ docker compose up --build
app-1  |                 ^
app-1  | SyntaxError: invalid syntax
app-1 exited with code 1

### Шаг 1: Подготовка папки
```bash
mkdir order-system && cd order-system
touch docker-compose.yml app.py requirements.txt
```

---

### Шаг 2: Написание Django-приложения (`main.py`)
Мы будем использовать Django в режиме «одного файла» (mini-app), чтобы упростить задачу для экзамена.

```python
import os
import django
from django.conf import settings
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone

# 1. Настройки
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'orders_db', 'USER': 'admin', 'PASSWORD': 'password', 'HOST': 'db', 'PORT': '5432',
        }},
        INSTALLED_APPS=[], # Оставляем пустым, чтобы не было рекурсии
        TIME_ZONE='UTC',
        USE_TZ=True,
        SECRET_KEY='fake-key',
        ROOT_URLCONF=__name__,
    )
    django.setup()

from django.db import models, connection

# 2. Модель (без привязки к приложению через app_label)
class Order(models.Model):
    item = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'app_order'
        app_label = 'main_app' # Любое имя, отличное от имени файла

# 3. Функции
def add_order(request):
    item_name = request.GET.get('item', 'Generic Item')
    order = Order.objects.create(item=item_name)
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

# 5. Приложение для сервера
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

if __name__ == "__main__":
    import uvicorn
    import time
    
    print("Ожидание базы данных (15 сек)...")
    time.sleep(15)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_order (
                id SERIAL PRIMARY KEY, 
                item VARCHAR(100), 
                created_at TIMESTAMP WITH TIME ZONE, 
                delivered_at TIMESTAMP WITH TIME ZONE
            );
        """)
    
    print("Старт сервера на http://localhost:8000")
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
