# beat.py (o en un archivo similar)

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import datetime, timedelta
from celery import Celery

app = Celery('estetica')

# Intervalo para la tarea (cada hora)
interval_schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.MINUTES
)

# Crear o actualizar la tarea periódica
PeriodicTask.objects.update_or_create(
    name='My Periodic Task',
    defaults={
        'task': 'myapp.tasks.my_periodic_task',
        'interval': interval_schedule,
        'start_time': datetime.utcnow(),  # Opcional: Hora de inicio
    }
)
