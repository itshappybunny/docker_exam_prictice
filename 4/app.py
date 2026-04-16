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