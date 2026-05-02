from celery import Celery

from src.config import settings


celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,  # Добавили Result Backend
    include=[
        "src.tasks.tasks",
    ],
)

celery_instance.conf.beat_schedule = {
    "daily-checkin-emails": {
        "task": "booking_today_checkin",
        "schedule": 86400.0,  # Раз в сутки (24 часа), а не 5 секунд
    }
}