from celery import Celery

from src.shared.config import settings

celery_app = Celery(
    "sentinel",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["src.scheduling.tasks"],
)

celery_app.conf.timezone = "UTC"
celery_app.conf.beat_scheduler = "redbeat.schedulers.RedBeatScheduler"
celery_app.conf.redbeat_redis_url = settings.REDIS_URL
celery_app.conf.beat_schedule = {}

# TODO: incomplete — no schedule entries defined yet; see src/scheduling/tasks.py
