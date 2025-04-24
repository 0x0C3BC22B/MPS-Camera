from django.http import JsonResponse
from .models import IPCamera

def list_cameras(request):
    cameras = IPCamera.objects()
    data = [{
        "name": cam.name,
        "ip_address": cam.ip_address,
        "mac": cam.mac,
        "serial_number": cam.serial_number,
        "model": cam.model.name if cam.model else None,
        "model_vendor": cam.model.vendor.name if cam.model and cam.model.vendor else None,
        "username": cam.username,
        "created_at": cam.created_at.isoformat(),
        "updated_at": cam.updated_at.isoformat(),
        "status": cam.status
    } for cam in cameras]
    return JsonResponse(data, safe=False)
