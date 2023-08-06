# celeryconfig.py
from datetime import timedelta

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"
timezone = "UTC"
beat_schedule = {
    "update-every-day": {
        "task": "app.main:update_database_task",
        "schedule": timedelta(days=1),
        "args": (),
    }
}
