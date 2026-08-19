from celery import Celery

from sentinel.shared.config import settings

celery_app = Celery(
    "sentinel",
    broker=settings.redis.redis_url,
    backend=settings.redis.redis_url,
    include=["sentinel.scheduling.tasks"],
)

celery_app.conf.timezone = "UTC"
celery_app.conf.beat_scheduler = "redbeat.schedulers.RedBeatScheduler"
celery_app.conf.redbeat_redis_url = settings.redis.redis_url
celery_app.conf.beat_schedule = {}

# TODO: incomplete — no schedule entries defined yet; see src/scheduling/tasks.py
