from celery import shared_task
import datetime

@shared_task
def my_periodic_task():
    print("La tarea programada se está ejecutando.")