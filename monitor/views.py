import datetime
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
import json
from .models import IPCamera, CameraModel, Vendors
from mongoengine.errors import DoesNotExist
from .models import IPCamera

@csrf_exempt
def list_cameras(request):
    cameras = IPCamera.objects()
    data = []
    for cam in cameras:
        models_info = [{
            "name": m.name,
            "vendors": [v.name for v in m.vendor]
        } for m in cam.model]

        data.append({
            "name": cam.name,
            "ip_address": cam.ip_address,
            "mac": cam.mac,
            "serial_number": cam.serial_number,
            "models": models_info,
            "username": cam.username,
            "created_at": cam.created_at.isoformat() if cam.created_at else None,
            "updated_at": cam.updated_at.isoformat() if cam.updated_at else None,
            "status": cam.status
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def create_ipcamera(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        camera_models = []
        for cm in data.get('model', []):
            vendors = [Vendors(**v) for v in cm.get('vendor', [])]
            camera_models.append(CameraModel(name=cm['name'], vendor=vendors))

        camera = IPCamera(
            name=data['name'],
            ip_address=data['ip_address'],
            port=data.get('port', 80),
            model=camera_models,
            created_at=datetime.datetime.utcnow(),
            mac=data.get('mac', ''),
            username=data.get('username', ''),
            password=data.get('password', ''),
            serial_number=data.get('serial_number', ''),
            status=data.get('status', 'inactive')
        )
        camera.save()
        return JsonResponse({'message': 'Camera created successfully', 'id': str(camera.id)})

@csrf_exempt
def get_ipcamera(request, camera_id):
    try:
        camera = IPCamera.objects.get(id=ObjectId(camera_id))
        camera_dict = camera.to_mongo().to_dict()
        camera_dict['_id'] = str(camera_dict['_id']) 
        return JsonResponse(camera_dict, safe=False)
    except IPCamera.DoesNotExist:
        return JsonResponse({'error': 'Camera not found'}, status=404)

@csrf_exempt
def update_ipcamera(request, camera_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            camera = IPCamera.objects.get(id=camera_id)
            # print(f"Original camera: {camera.to_json()}")

            for key, value in data.items():
                if key == 'model':
                    camera_models = []
                    for cm in value:
                        vendors = [Vendors(**v) for v in cm.get('vendor', [])]
                        camera_models.append(CameraModel(name=cm['name'], vendor=vendors))
                    camera.model = camera_models
                elif hasattr(camera, key):
                    setattr(camera, key, value)
                else:
                    print(f"WARNING: Invalid field '{key}' ignored.")

            camera.save()
            # print(f"Updated camera: {camera.to_json()}")
            return JsonResponse({'message': 'Camera updated successfully'})

        except IPCamera.DoesNotExist:
            return JsonResponse({'error': 'Camera not found'}, status=404)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def delete_ipcamera(request, camera_id):
    if request.method == 'DELETE':
        try:
            camera = IPCamera.objects.get(id=camera_id)
            camera.delete()
            return JsonResponse({'message': 'Camera deleted successfully'})
        except DoesNotExist:
            return JsonResponse({'error': 'Camera not found'}, status=404)
