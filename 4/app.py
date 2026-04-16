import os
import django
from django.conf import settings
from django.db import models, connection
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

# Настройки Django
if not settings.configured:
    settings.configure(
        DATABASES={'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'orders_db', 'USER': 'admin', 'PASSWORD': 'password', 'HOST': 'db', 'PORT': '5432',
        }},
        INSTALLED_APPS=('app',),
        TIME_ZONE='UTC',
        USE_TZ=True,
    )
    django.setup()

# Модель заказа
class Order(models.Model):
    item = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)

    class Meta: app_label = 'app'

# --- API эндпоинты ---
from django.urls import path

def add_order(request):
    item_name = request.GET.get('item', 'Generic Item')
    order = Order.objects.create(item=item_name)
    # Имитируем, что заказ доставлен через случайное время (для теста)
    order.delivered_at = order.created_at + timedelta(hours=2) 
    order.save()
    return JsonResponse({"status": "Заказ создан", "id": order.id})

def delivery_report(request):
    # Расчет среднего времени доставки
    orders = Order.objects.exclude(delivered_at__isnull=True)
    if not orders.exists():
        return JsonResponse({"average_delivery_hours": 0})
    
    total_time = sum([(o.delivered_at - o.created_at).total_seconds() for o in orders])
    avg_hours = (total_time / len(orders)) / 3600
    return JsonResponse({"avg_delivery_time_hours": avg_hours})

urlpatterns = [
    path('add/', add_order),
    path('report/', delivery_report),
]

# Запуск
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    # Авто-создание таблиц перед запуском
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS app_order (id SERIAL PRIMARY KEY, item VARCHAR(100), created_at TIMESTAMP, delivered_at TIMESTAMP);")
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    import uvicorn
    uvicorn.run(application, host="0.0.0.0", port=8000)