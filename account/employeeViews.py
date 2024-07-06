from datetime import datetime

import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from account.models import CustomUser, StaffPosition, EmployeeStatus, EmployeeType, Gender
from university.models import Department, University


def employee_list_json(request):
    employees = CustomUser.objects.filter(is_employee=True)

    # Prepare JSON data
    data = []
    for employee in employees:
        employee_data = {
            'id': employee.id,
            'full_name': employee.full_name,
            'email': employee.email,
            'phone_number': employee.phone_number,
            'image': employee.imageFile.url if employee.imageFile else None,
            'status': "Active" if employee.is_active else "Inactive",
            'join_date': employee.created_at.strftime('%Y-%m-%d'),
            'birth_date': employee.birth_date.strftime('%Y-%m-%d') if employee.birth_date else None,
            'employee_id_number': employee.employee_id_number,
            'user_type': employee.get_user_type_display(),
            'hemis_role': [role.name for role in employee.hemis_role.all()],
            'created_at': employee.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': employee.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': employee.last_login.strftime('%Y-%m-%d %H:%M:%S'),
            'last_activity': employee.last_activity.strftime('%Y-%m-%d %H:%M:%S') if employee.last_activity else None,
            # Add other fields as needed
        }
        data.append(employee_data)

    # Return JSON response
    return JsonResponse(data, safe=False)

def update_or_create(model, filter_kwargs, defaults=None):
    obj, created = model.objects.get_or_create(**filter_kwargs, defaults=defaults)
    if not created and defaults:
        for key, value in defaults.items():
            setattr(obj, key, value)
        obj.save()
    return obj, created

def create_employee_from_api(request):
    try:
        # University modelinde is_active alanı True olan bir nesneyi alın
        university = University.objects.get(is_active=True)
        api_url = university.api_url  # API URL'sini alın
        api_token = university.api_token  # API Token'ını alın
        url = f'{api_url}data/employee-list?type=all'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {api_token}'  # API Token'ını Authorization başlığına ekleyin
        }

        # cURL so'rovi uchun parametrlar
        employee_id_number = request.POST.get('employee_id_number')
        params = {
            'search': employee_id_number
        }
        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()

                for item in data.get('data', {}).get('items', []):
                    staffPosition_name = item.get('staffPosition', {}).get('name')
                    staffPosition_code = item.get('staffPosition', {}).get('code')
                    defaults = {'code': staffPosition_code}
                    obj, created = update_or_create(
                        StaffPosition,
                        filter_kwargs={'name': staffPosition_name},
                        defaults=defaults
                    )

                for item in data.get('data', {}).get('items', []):
                    employeeStatus_name = item.get('employeeStatus', {}).get('name')
                    employeeStatus_code = item.get('employeeStatus', {}).get('code')
                    defaults = {'code': employeeStatus_code}
                    obj, created = update_or_create(
                        EmployeeStatus,
                        filter_kwargs={'name': employeeStatus_name},
                        defaults=defaults
                    )

                for item in data.get('data', {}).get('items', []):
                    employeeType_name = item.get('employeeType', {}).get('name')
                    employeeType_code = item.get('employeeType', {}).get('code')
                    defaults = {'code': employeeType_code}
                    obj, created = update_or_create(
                        EmployeeType,
                        filter_kwargs={'name': employeeType_name},
                        defaults=defaults
                    )

                if 'data' in data:
                    item = data['data']['items'][0]

                    employeeStatus_code = item.get('employeeStatus', {}).get('code')
                    employeeStatus, _ = EmployeeStatus.objects.get_or_create(code=employeeStatus_code)

                    employeeType_code = item.get('employeeType', {}).get('code')
                    employeeType, _ = EmployeeType.objects.get_or_create(code=employeeType_code)

                    StaffPosition_code = item.get('staffPosition', {}).get('code')
                    staffPosition, _ = StaffPosition.objects.get_or_create(code=StaffPosition_code)

                    gender_code = item.get('gender', {}).get('code')
                    gender, _ = Gender.objects.get_or_create(code=gender_code)

                    department_id = item.get('department', {}).get('id')
                    department, _ = Department.objects.get_or_create(codeID=department_id)

                    contract_date_timestamp = item.get('contract_date')
                    contract_date = datetime.utcfromtimestamp(contract_date_timestamp)

                    created_at_timestamp = item.get('created_at')
                    created_at = datetime.utcfromtimestamp(created_at_timestamp)

                    updated_at_timestamp = item.get('updated_at')
                    updated_at = datetime.utcfromtimestamp(updated_at_timestamp)

                    image_url = item.get('image')

                    existing_user = CustomUser.objects.filter(employee_id_number=employee_id_number).first()
                    if existing_user:
                        existing_user.full_name = item.get('full_name', '')
                        existing_user.short_name = item.get('short_name', '')
                        existing_user.first_name = item.get('first_name', '')
                        existing_user.second_name = item.get('second_name', '')
                        existing_user.third_name = item.get('third_name', '')
                        existing_user.employee_id_number = item.get('employee_id_number', '')
                        existing_user.full_id = item.get('employee_id_number', '')
                        existing_user.image = image_url
                        existing_user.gender = gender
                        existing_user.employeeStatus = employeeStatus
                        existing_user.employeeType = employeeType
                        existing_user.staffPosition = staffPosition
                        existing_user.department = department
                        existing_user.contractDate = contract_date
                        existing_user.created_at = created_at
                        existing_user.updated_at = updated_at
                        existing_user.hash = item.get('hash', '')
                        existing_user.user_type = 2
                        existing_user.is_student = False
                        existing_user.is_active = True
                        existing_user.save()

                        return JsonResponse({'success': True, 'message': 'Foydalanuvchi ma\'lumotlari yangilandi'},
                                            status=200)
                    else:
                        user, created = CustomUser.objects.get_or_create(
                            username=(item.get('first_name', '') + '_' + item.get('second_name', '') + str(
                                item.get('id', ''))).lower(),
                            email=(item.get('employee_id_number', '') + '@namdpi.uz').lower(),
                            defaults={
                                'full_name': item.get('full_name', ''),
                                'short_name': item.get('short_name', ''),
                                'first_name': item.get('first_name', ''),
                                'second_name': item.get('second_name', ''),
                                'third_name': item.get('third_name', ''),
                                'employee_id_number': item.get('employee_id_number', ''),
                                'full_id': item.get('employee_id_number', ''),
                                'image': image_url,
                                'employeeStatus': employeeStatus,
                                'employeeType': employeeType,
                                'staffPosition': staffPosition,
                                'password_save': (str(item.get('employee_id_number', '')) + 'namdpi'),
                                'department': department,
                                'contractDate': contract_date,
                                'created_at': created_at,
                                'updated_at': updated_at,
                                'hash': item.get('hash', ''),
                                'user_type': 2,
                                'is_student': False,
                                'is_active': True,
                            }
                        )

                    if created:
                        password = make_password(str(item.get('employee_id_number')) + 'namdpi')
                        user.set_password(password)
                        user.save()
                        username = (item.get('first_name', '') + '_' + item.get('second_name', '') + str(
                            item.get('id', ''))).lower()

                        user = authenticate(request, email=username, password=password)
                        if user is not None:
                            login(request, user)
                            return JsonResponse({'success': True, 'message': 'Tizimga muvaffaqiyatli kirdingiz'},
                                                status=200)
                    return JsonResponse({'success': True, 'message': 'Ma\'lumotlar muvaffaqiyatli saqlandi'},
                                        status=201)
                else:
                    return JsonResponse({'success': False, 'message': 'Ma\'lumotlar topilmadi'}, status=404)
            else:
                return JsonResponse({'success': False, 'message': 'Ma\'lumotlar olishda xatolik'}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    except University.DoesNotExist:
        print("Active university not found.")
        return HttpResponse("Active university not found.", status=404)

def get_employee_info(request):
    try:
        employee_id_number = request.GET.get('employee_id_number')
        # University modelinde is_active alanı True olan bir nesneyi alın
        university = University.objects.get(is_active=True)
        api_url = university.api_url  # API URL'sini alın
        api_token = university.api_token  # API Token'ını alın
        url = f'{api_url}data/employee-list?type=all&search={employee_id_number}'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {api_token}'  # API Token'ını Authorization başlığına ekleyin
        }

        # API ga so'rov tashlash
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            employee_info = response.json()
            if CustomUser.objects.filter(employee_id_number=employee_id_number).exists():
                return JsonResponse(employee_info, status=200)
            return JsonResponse(employee_info, status=201)
        else:
            # Agar so'rov muvaffaqiyatsiz bo'lsa, xatolarni qaytarish
            return JsonResponse({'error': 'Foydalanuvchi malumotlarini olishda xatolik yuz berdi'}, status=500)
    except University.DoesNotExist:
        print("Active university not found.")
        return HttpResponse("Active university not found.", status=404)