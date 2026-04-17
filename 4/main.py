import os
import django
from django.conf import settings
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
import time

# 1. Настройки
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'orders_db', 
            'USER': 'admin', 
            'PASSWORD': 'password', 
            'HOST': 'db', 
            'PORT': '5432',
        }},
        INSTALLED_APPS=[
            '__main__',  # Добавляем текущий модуль как приложение
        ],
        TIME_ZONE='UTC',
        USE_TZ=True,
        SECRET_KEY='fake-key-for-development',
        ROOT_URLCONF=__name__,
    )
    django.setup()

from django.db import models, connection
from django.urls import path
from django.core.handlers.asgi import ASGIHandler  # Исправлено: handlers вместо handleers

# 2. Модель
class Order(models.Model):
    item = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'app_order'
        app_label = '__main__'
    
    def __str__(self):
        return f"Order {self.id}: {self.item}"

# 3. Функции для создания таблицы
def init_db():
    """Создание таблицы если не существует"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_order (
                id SERIAL PRIMARY KEY, 
                item VARCHAR(100) NOT NULL, 
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(), 
                delivered_at TIMESTAMP WITH TIME ZONE NULL
            );
        """)
    print("✅ Таблица app_order проверена/создана")

# 4. Views
def add_order(request):
    item_name = request.GET.get('item', 'Generic Item')
    order = Order.objects.create(item=item_name)
    order.delivered_at = timezone.now() + timedelta(hours=2)
    order.save()
    return JsonResponse({"status": "Заказ создан", "id": order.id, "item": order.item})

def delivery_report(request):
    orders = Order.objects.exclude(delivered_at__isnull=True)
    if not orders.exists():
        return JsonResponse({"average_delivery_hours": 0})
    
    total_seconds = sum([(o.delivered_at - o.created_at).total_seconds() for o in orders])
    avg_hours = (total_seconds / len(orders)) / 3600
    return JsonResponse({"average_delivery_time_hours": round(avg_hours, 2), "total_orders": len(orders)})

# 5. Роуты
urlpatterns = [
    path('add/', add_order, name='add_order'),
    path('report/', delivery_report, name='delivery_report'),
]

# 6. Приложение для сервера
application = ASGIHandler()

if __name__ == "__main__":
    import uvicorn
    
    print("🟡 Ожидание базы данных (10 сек)...")
    time.sleep(10)
    
    # Инициализация базы данных
    init_db()
    
    print("🚀 Старт сервера на http://0.0.0.0:8000")
    print("📝 Примеры запросов:")
    print("  - curl 'http://localhost:8000/add/?item=Телефон'")
    print("  - curl 'http://localhost:8000/add/'")
    print("  - curl 'http://localhost:8000/report/'")
    print("-" * 50)
    
    uvicorn.run(application, host="0.0.0.0", port=8000, log_level="info")