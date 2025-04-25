import requests
import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

def camera_list(request):
    try:
        response = requests.get("http://localhost:8000/api/ipcameras/")  
        cameras = response.json()
    except Exception as e:
        cameras = []
        print(f"Error fetching cameras: {e}")

    search = request.GET.get('search', '')
    if search:
        cameras = [cam for cam in cameras if search.lower() in cam['name'].lower()]

    paginator = Paginator(cameras, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.GET.get('export') == 'excel':
        return export_to_excel(cameras)

    return render(request, 'webclient/camera_list.html', {'page_obj': page_obj, 'search': search})


def export_to_excel(cameras):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cámaras"

    columns = ['ID', 'Nombre', 'Dirección IP', 'Estado', 'MAC', 'Modelos', 'Vendors']
    ws.append(columns)

    for cam in cameras:
        models = cam.get('model', [])
        model_names = ', '.join([m.get('name', 'N/A') for m in models])

        vendors = []
        for m in models:
            vendors += [v.get('name', 'N/A') for v in m.get('vendor', [])]
        vendor_names = ', '.join(vendors)

        row = [
            cam.get('id', 'N/A'),
            cam.get('name', 'N/A'),
            cam.get('ip_address', 'N/A'),
            cam.get('status', 'N/A'),
            cam.get('mac', 'N/A'),
            model_names or 'N/A',
            vendor_names or 'N/A'
        ]
        ws.append(row)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=cameras.xlsx'
    wb.save(response)
    return response