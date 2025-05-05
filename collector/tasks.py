from celery import shared_task
from collector.jobs.camera_collector import update_camera_info

@shared_task
def actualizar_info_camaras():
    update_camera_info()