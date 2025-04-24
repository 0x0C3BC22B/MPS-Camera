import datetime
import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
from monitor.models import IPCamera  

NAMESPACE = {'hik': 'http://www.hikvision.com/ver20/XMLSchema'}

IMAGE_CHANNEL_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ImageChannel xmlns="http://www.hikvision.com/ver20/XMLSchema" version="2.0">
    <id>1</id>
    <enabled>true</enabled>
    <videoInputID>1</videoInputID>
</ImageChannel>
"""

def update_camera_info():
    cameras = IPCamera.objects.all()

    for cam in cameras:
        auth = HTTPDigestAuth(cam.username, cam.password)
        base_url = f"http://{cam.ip_address}:{cam.port}"

        try:
            # ---- 1. Obtener información del dispositivo ----
            info_url = f"{base_url}/ISAPI/System/deviceInfo"
            response_info = requests.get(info_url, auth=auth, timeout=5)

            if response_info.status_code == 200:
                root = ET.fromstring(response_info.text)
                cam.name = root.find('hik:deviceName', NAMESPACE).text
                cam.serial_number = root.find('hik:serialNumber', NAMESPACE).text
                cam.mac = root.find('hik:macAddress', NAMESPACE).text

            # ---- 2. Configurar canal de imagen para obtener status ----
            image_url = f"{base_url}/ISAPI/Image/channels/1"
            response_image = requests.put(
                image_url,
                data=IMAGE_CHANNEL_XML,
                headers={"Content-Type": "application/xml"},
                auth=auth,
                timeout=5
            )

            if response_image.status_code == 200:
                root = ET.fromstring(response_image.text)
                status_string = root.find('hik:statusString', NAMESPACE).text

                # Guardamos el status string tal cual lo devuelve el dispositivo (ej: OK, Error, etc.)
                cam.status = status_string
            else:
                cam.status = "ERROR PUT"

        except Exception as e:
            cam.status = "UNREACHABLE"
            print(f"[ERROR] {cam.ip_address}: {e}")

        cam.updated_at = datetime.datetime.utcnow()
        cam.save()
        print(f"[✓] {cam.ip_address} => {cam.status}")
