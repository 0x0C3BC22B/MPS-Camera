from django.core.management.base import BaseCommand
from collector.jobs.camera_collector import update_camera_info


class Command(BaseCommand):
    help = 'Actualiza la información de todas las cámaras'

    def handle(self, *args, **kwargs):
        update_camera_info()