from celery import shared_task

@shared_task
def periodic_alerts_task():
    send_alerts()
