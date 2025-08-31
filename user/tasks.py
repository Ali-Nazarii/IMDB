from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_daily_email():
    users = User.objects.all()
    for user in users:
        print(f"Hey {user.username}! Come watch a movie and give your rating!")
