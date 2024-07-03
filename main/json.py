import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .models import NetworkDevice
from .utils import get_network_devicess


def device_list(request):
    devices = get_network_devices()
    return JsonResponse({'devices': devices})

def get_network_devices(request):
    devices = NetworkDevice.objects.all()

    device_list = []
    for device in devices:
        device_info = {
            'ip_address': device.ip_address,
            'mac_address': device.mac_address,
            'manufacturer': device.manufacturer,
            'status': device.status,
            'user_name': device.user_name,
            'device_name': device.device_name
        }
        device_list.append(device_info)

    return JsonResponse({'devices': device_list})

def get_network_allow_devices(request):
    # Tasdiqlangan qurilmalarni filtrlaymiz
    devices = NetworkDevice.objects.filter(status='Tasdiqlangan')

    device_list = []
    for device in devices:
        # Qurilma ma'lumotlarini olish va ro'yxatga qo'shish
        device_info = {
            'ip_address': device.ip_address,
            'mac_address': device.mac_address,
            'manufacturer': device.manufacturer,
            'status': device.status,
            'user_name': device.user_name,
            'device_name': device.device_name
        }
        device_list.append(device_info)

    # Tasdiqlangan qurilmalar ro'yxatini JSON formatida qaytarish
    return JsonResponse({'devices': device_list})

def get_network_deny_devices(request):
    # Taqiqlangan qurilmalarni filtrlaymiz
    devices = NetworkDevice.objects.filter(status='Ta\'qiqlangan')

    device_list = []
    for device in devices:
        # Qurilma ma'lumotlarini olish va ro'yxatga qo'shish
        device_info = {
            'ip_address': device.ip_address,
            'mac_address': device.mac_address,
            'manufacturer': device.manufacturer,
            'status': device.status,
            'user_name': device.user_name,
            'device_name': device.device_name
        }
        device_list.append(device_info)

    # Taqiqlangan qurilmalar ro'yxatini JSON formatida qaytarish
    return JsonResponse({'devices': device_list})



@csrf_exempt  # CSRF ni ochirish
def save_all_devices(request):
    if request.method == 'POST':
        try:
            # JSON ma'lumotlarini yuklash
            devices = get_network_devicess()
            saved_count = 0

            for device_data in devices:
                ip_address = device_data.get('ip_address')
                mac_address = device_data.get('mac_address')
                manufacturer = device_data.get('manufacturer')

                # IP manzil va MAC manzil bo'yicha qurilma bazada mavjudligini tekshiramiz
                existing_device = NetworkDevice.objects.filter(ip_address=ip_address, mac_address=mac_address).first()

                if existing_device:
                    # Agar mavjud bo'lsa, manufacturer ni yangilaymiz
                    existing_device.manufacturer = manufacturer
                    existing_device.save()
                    saved_count += 1  # Yangilangan qurilmalar sonini hisoblash
                else:
                    # Agar mavjud bo'lmasa, yangi qurilmani yaratamiz
                    NetworkDevice.objects.create(
                        ip_address=ip_address,
                        mac_address=mac_address,
                        manufacturer=manufacturer,
                        status='Tasdiqlanmagan'
                    )
                    saved_count += 1  # Yaratilgan qurilmalar sonini hisoblash

            return JsonResponse({'message': f'{saved_count} ta qurilma ma\'lumotlari muvaffaqiyatli saqlandi'}, status=200)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')
    else:
        return JsonResponse({'error': 'Faqat POST so\'rov qabul qilinadi'}, status=405)


@csrf_exempt
def update_device_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip_address = data.get('ip_addresses', None)  # Tugma yoki tugmalarning IP manzili
            print(ip_address)

            if ip_address:
                print(ip_address)
                ip_address = ip_address[0]
                # Qidirish va yangilash
                device = NetworkDevice.objects.filter(ip_address=ip_address).first()
                print(device)
                if device:
                    if device.status == 'Tasdiqlangan':
                        device.status = 'Tasdiqlanmagan'  # Agar hozirgi status 'Tasdiqlangan' bo'lsa 'Tasdiqlanmagan' ga o'zgartiramiz
                    else:
                        device.status = 'Tasdiqlangan'  # Agar hozirgi status 'Tasdiqlanmagan' yoki boshqa bo'lsa 'Tasdiqlangan' ga o'zgartiramiz
                    device.save()

                return JsonResponse({'success': True, 'message': f'"{ip_address}" IP manzilidagi qurilma muvaffaqiyatli yangilandi'})
            else:
                return JsonResponse({'success': False, 'message': 'IP manzili berilmagan'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Server xatosi: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Faqat POST so\'rovlarni qabul qilamiz'}, status=405)