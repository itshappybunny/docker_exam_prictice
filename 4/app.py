import os
import django
from django.conf import settings
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone

# 1. Настройки (ВАЖНО: добавляем __name__ в INSTALLED_APPS)
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'orders_db', 'USER': 'admin', 'PASSWORD': 'password', 'HOST': 'db', 'PORT': '5432',
        }},
        INSTALLED_APPS=['app'], # Имя должно совпадать с именем файла (app.py)
        TIME_ZONE='UTC',
        USE_TZ=True,
        SECRET_KEY='fake-key',
        ROOT_URLCONF=__name__, # Указываем, что роуты искать в этом же файле
    )
    django.setup()

# 2. Модели
from django.db import models, connection

class Order(models.Model):
    item = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)

    class Meta:
        app_label = 'app' # Должно совпадать с именем файла без .py
        managed = False 
        db_table = 'app_order'

# 3. View-функции
def add_order(request):
    item_name = request.GET.get('item', 'Generic Item')
    order = Order.objects.create(item=item_name)
    order.delivered_at = timezone.now() + timedelta(hours=2)
    order.save()
    return JsonResponse({"status": "Заказ создан", "id": order.id}, json_dumps_params={'ensure_ascii': False})

def delivery_report(request):
    orders = Order.objects.exclude(delivered_at__isnull=True)
    if not orders.exists():
        return JsonResponse({"average_delivery_hours": 0})
    
    total_seconds = sum([(o.delivered_at - o.created_at).total_seconds() for o in orders])
    avg_hours = (total_seconds / len(orders)) / 3600
    return JsonResponse({"avg_delivery_time_hours": round(avg_hours, 2)})

# 4. Роуты (URLS)
from django.urls import path
urlpatterns = [
    path('add/', add_order),
    path('report/', delivery_report),
]

# 5. Точка входа
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

if __name__ == "__main__":
    import time
    import uvicorn
    
    # Даем базе время (10 секунд для уверенности)
    print("Ожидаем базу данных...")
    time.sleep(10)
    
    # Создаем таблицу
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_order (
                id SERIAL PRIMARY KEY, 
                item VARCHAR(100), 
                created_at TIMESTAMP WITH TIME ZONE, 
                delivered_at TIMESTAMP WITH TIME ZONE
            );
        """)
    print("Таблица готова. Запуск сервера...")
    uvicorn.run("__main__:application", host="0.0.0.0", port=8000, reload=True)