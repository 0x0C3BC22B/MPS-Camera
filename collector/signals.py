from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

@receiver(post_migrate)
def crear_tarea_periodica(sender, **kwargs):
    if sender.name != "collector":
        return

    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    PeriodicTask.objects.update_or_create(
        name='Actualizar info de cámaras',
        defaults={
            'interval': schedule,
            'task': 'collector.tasks.actualizar_info_camaras',
            'args': json.dumps([]),
        }
    )
