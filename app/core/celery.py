from celery import Celery
from app.core.config import settings


celery_app = Celery(
    "jobtracker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)


celery_app.autodiscover_tasks(
    packages=["app.tasks"],
    force=True
)

celery_app.conf.beat_schedule = {
    "parse-every-5-minutes": {
        "task": "app.tasks.vacancies.parse_vacancies",
        "schedule": 300.0,
    },
}

celery_app.conf.timezone = "UTC"
