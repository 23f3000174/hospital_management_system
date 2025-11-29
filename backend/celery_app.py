from celery import Celery

celeryApp = Celery(
    'task', 
    broker='redis://localhost:6379/0    '
)
celeryApp.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)

from mail import send_mail
from app import create_app
from models.models import User

@celeryApp.task()
def daily_reminder():
    app = create_app()
    with app.app_context():
        for user in User.query.all():
            to = user.email
            subject = "Daily Reminder"
            body = f"Hello {user.full_name}, this is your daily Reminder to take care of your health"
            send_mail(to, subject, body)
    return "Daily remainder sent!!"

from celery.schedules import crontab
import datetime

celeryApp.conf.beat_schedule = {
    'daily_reminders': {
        'task': 'celery_app.daily_reminder',
        'schedule': crontab(hour=16, minute=53) # every day
        # 'schedule': datetime.timedelta(seconds=3) # every 3 seconds
    },
    'montly_reminders': {
        'task': 'celery_app.monthly_reminder',
        'schedule': crontab(day_of_month=2, hour=16, minute=30)
    }
}
