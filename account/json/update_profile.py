import sys
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from account.models import Gender, Country, Province, District, Citizenship, Accommodation, CustomUser, AcademicRank, \
    AcademicDegree, EmploymentForm, EmploymentStaff, StaffPosition, EmployeeStatus, EmployeeType
from university.models import University, Department, Specialty, Curriculum, GroupUniver, EducationYear
import requests



@login_required
def update_passport_serial(request):
    if request.method == 'POST':
        passport_serial = request.POST.get('passportSerial')
        # Probeldan ochirish
        passport_serial = passport_serial.replace(" ", "")
        # Tekshirish: Passport seriyasi boshida 2 ta harf va keyin 7 ta raqam bo'lishi kerak
        if len(passport_serial) != 9 or not passport_serial[:2].isalpha() or not passport_serial[2:].isdigit():
            return JsonResponse({'error': 'Pasport seriayasi noto\'g\'ri formatda'}, status=400)

        request.user.passport_serial = passport_serial
        request.user.save()
        return JsonResponse({'success': True, 'message': 'Pasport ma\'lumotlari muvaffaqiyatli yangilandi'})
    else:
        return JsonResponse({'error': 'GET so\'rov qabul qilinmaydi'}, status=400)


@login_required
def update_passport_jshshir(request):
    if request.method == 'POST':
        passportjshshir = request.POST.get('passportjshshir')

        if not passportjshshir:
            return JsonResponse({'error': 'Pasport seriayasi kiritilmagan'}, status=400)

        # Tekshirish: Passport seriyasi faqat 14 ta belgidan iborat bo'lishi kerak
        if len(passportjshshir) != 14:
            return JsonResponse({'error': 'Pasport seriayasi noto\'g\'ri formatda'}, status=400)

        request.user.passport_jshshir = passportjshshir
        request.user.save()
        return JsonResponse({'success': True, 'message': 'Pasport ma\'lumotlari muvaffaqiyatli yangilandi'})
    else:
        return JsonResponse({'error': 'GET so\'rov qabul qilinmaydi'}, status=400)


@login_required
def update_social_media(request):
    if request.method == 'POST':
        # Post so'rovi orqali ma'lumotlarni olish
        telegram = request.POST.get('social-tg')
        instagram = request.POST.get('social-insta')
        facebook = request.POST.get('social-fb')

        # Profil ma'lumotlarini yangilash
        request.user.telegram = telegram
        request.user.instagram = instagram
        request.user.facebook = facebook
        request.user.save()

        return JsonResponse({'success': True, 'message': 'Profil ma\'lumotlari muvaffaqiyatli yangilandi'})
    else:
        return JsonResponse({'error': 'GET so\'rov qabul qilinmaydi'}, status=400)


@login_required
def update_employee_profile_from_api(request):
    try:
        university = University.objects.get(is_active=True)
    except University.DoesNotExist:
        print("Active university not found.")
        return JsonResponse({"success": False, "message": "Active university not found."}, status=404)

    api_url = university.api_url
    api_token = university.api_token
    url = f'{api_url}data/employee-list'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    employee_id_number = request.POST.get('employee_id_number')
    params = {'search': employee_id_number, 'type': 'all'}  # 'all' ni quti ichiga olingan

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()  # JSON ko'rinishida javobni olish
            item = data['data']['items'][0]  # api dan kelgan ma'lumotlar

            # Jinsi
            gender_code = item.get('gender', {}).get('code')
            gender_name = item.get('gender', {}).get('name')
            gender, _ = Gender.objects.get_or_create(code=gender_code, name=gender_name)
            print('gender')
            # Ilmit unvonni aniqlash
            academicRank_code = item.get('academicRank', {}).get('code')
            academicRank_name = item.get('academicRank', {}).get('name')
            academicRank, _ = AcademicRank.objects.get_or_create(code=academicRank_code, name=academicRank_name)
            print('Ilmiy daraja')
            # Ilmit unvonni aniqlash
            academicDegree_code = item.get('academicDegree', {}).get('code')
            academicDegree_name = item.get('academicDegree', {}).get('name')
            academicDegree, _ = AcademicDegree.objects.get_or_create(code=academicDegree_code, name=academicDegree_name)
            print('Ilmiy unvon')
            # Ilmit unvonni aniqlash
            employmentForm_code = item.get('employmentForm', {}).get('code')
            employmentForm_name = item.get('employmentForm', {}).get('name')
            employmentForm, _ = EmploymentForm.objects.get_or_create(code=employmentForm_code, name=employmentForm_name)
            print('Bandlik shakli')
            employmentStaff_code = item.get('employmentStaff', {}).get('code')
            employmentStaff_name = item.get('employmentStaff', {}).get('name')
            employmentStaff, _ = EmploymentStaff.objects.get_or_create(code=employmentStaff_code, name=employmentStaff_name)
            print('Bandlik Hodimlar')
            staffPosition_code = item.get('staffPosition', {}).get('code')
            staffPosition_name = item.get('staffPosition', {}).get('name')
            staffPosition, _ = StaffPosition.objects.get_or_create(code=staffPosition_code, name=staffPosition_name)
            print('Hodim orni')
            employeeStatus_code = item.get('employeeStatus', {}).get('code')
            employeeStatus_name = item.get('employeeStatus', {}).get('name')
            employeeStatus, _ = EmployeeStatus.objects.get_or_create(code=employeeStatus_code, name=employeeStatus_name)
            print('Hodim holati')
            employeeType_code = item.get('employeeType', {}).get('code')
            employeeType_name = item.get('employeeType', {}).get('name')
            employeeType, _ = EmployeeType.objects.get_or_create(code=employeeType_code, name=employeeType_name)
            print('Hodim holati')
            # Bo'limni aniqlash
            department_id = item.get('department', {}).get('id')
            department, _ = Department.objects.get_or_create(codeID=department_id)
            print('department')
            # created_at
            created_at_timestamp = item.get('created_at')
            created_at = datetime.utcfromtimestamp(created_at_timestamp)
            print('created at')
            # updated_at
            updated_at_timestamp = item.get('updated_at')
            updated_at = datetime.utcfromtimestamp(updated_at_timestamp)
            print('updated at')
            # contract_date
            contract_date_timestamp = item.get('contract_date')
            contract_date = datetime.utcfromtimestamp(contract_date_timestamp)
            print('updated at')
            # birth_date
            birth_date_timestamp = item.get('birth_date')
            birth_date = datetime.utcfromtimestamp(birth_date_timestamp)
            print('updated at')
            # Foydalanuvchi ma'lumotlarini yangilash
            user = CustomUser.objects.get(employee_id_number=item['employee_id_number'])  # foydalanuvchi obyekti
            user.full_name = item['full_name']
            user.short_name = item['short_name']
            user.first_name = item['first_name']
            user.second_name = item['second_name']
            user.third_name = item['third_name']
            user.gender = gender
            user.birth_date = birth_date
            user.student_id_number = item.get('employee_id_number', '')
            user.full_id = item.get('employee_id_number', '')
            user.gender = gender
            user.academicDegree = academicDegree
            user.academicRank = academicRank
            user.employmentForm = employmentForm
            user.employmentStaff = employmentStaff
            user.staffPosition = staffPosition
            user.employeeStatus = employeeStatus
            user.employeeType = employeeType
            user.department = department
            user.created_at = created_at
            user.updated_at = updated_at
            user.year_of_enter = item.get('year_of_enter', '')
            user.contractDate = contract_date
            user.hash = item.get('hash', '')
            user.is_student = False
            user.is_employee = True
            user.is_active = True
            user.is_followers_book = True
            user.save()

            return JsonResponse({'success': True, 'message': 'Foydalanuvchi ma\'lumotlari yangilandi'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Ma\'lumotlar olishda xatolik'}, status=500)
    except Exception as e:
        print(sys.exc_info())
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
def update_student_profile_from_api(request):
    try:
        university = University.objects.get(is_active=True)
    except University.DoesNotExist:
        print("Active university not found.")
        return JsonResponse({"success": False, "message": "Active university not found."}, status=404)

    api_url = university.api_url
    api_token = university.api_token
    url = f'{api_url}data/employee-list'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    employee_id_number = request.POST.get('employee_id_number')
    params = {'search': employee_id_number, 'type': 'all'}  # 'all' ni quti ichiga olingan

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()  # JSON ko'rinishida javobni olish
            item = data['data']['items'][0]  # api dan kelgan ma'lumotlar

            # Jinsi
            gender_code = item.get('gender', {}).get('code')
            gender_name = item.get('gender', {}).get('name').lower()
            gender, _ = Gender.objects.get_or_create(code=gender_code, name=gender_name)
            print('gender')
            # Ilmit unvonni aniqlash
            academicRank_code = item.get('academicRank', {}).get('code')
            academicRank_name = item.get('academicRank', {}).get('name')
            academicRank, _ = AcademicRank.objects.get_or_create(code=academicRank_code, name=academicRank_name)
            print('Ilmiy daraja')
            # Ilmit unvonni aniqlash
            academicDegree_code = item.get('academicDegree', {}).get('code')
            academicDegree_name = item.get('academicDegree', {}).get('name')
            academicDegree, _ = AcademicDegree.objects.get_or_create(code=academicDegree_code, name=academicDegree_name)
            print('Ilmiy unvon')
            # Ilmit unvonni aniqlash
            employmentForm_code = item.get('employmentForm', {}).get('code')
            employmentForm_name = item.get('employmentForm', {}).get('name')
            employmentForm, _ = EmploymentForm.objects.get_or_create(code=employmentForm_code, name=employmentForm_name)
            print('Bandlik shakli')
            employmentStaff_code = item.get('employmentStaff', {}).get('code')
            employmentStaff_name = item.get('employmentStaff', {}).get('name')
            employmentStaff, _ = EmploymentStaff.objects.get_or_create(code=employmentStaff_code, name=employmentStaff_name)
            print('Bandlik Hodimlar')
            staffPosition_code = item.get('staffPosition', {}).get('code')
            staffPosition_name = item.get('staffPosition', {}).get('name')
            staffPosition, _ = StaffPosition.objects.get_or_create(code=staffPosition_code, name=staffPosition_name)
            print('Hodim orni')
            employeeStatus_code = item.get('employeeStatus', {}).get('code')
            employeeStatus_name = item.get('employeeStatus', {}).get('name')
            employeeStatus, _ = EmployeeStatus.objects.get_or_create(code=employeeStatus_code, name=employeeStatus_name)
            print('Hodim holati')
            employeeType_code = item.get('employeeType', {}).get('code')
            employeeType_name = item.get('employeeType', {}).get('name')
            employeeType, _ = EmployeeType.objects.get_or_create(code=employeeType_code, name=employeeType_name)
            print('Hodim holati')
            # Bo'limni aniqlash
            department_id = item.get('department', {}).get('id')
            department, _ = Department.objects.get_or_create(codeID=department_id)
            print('department')
            # created_at
            created_at_timestamp = item.get('created_at')
            created_at = datetime.utcfromtimestamp(created_at_timestamp)
            print('created at')
            # updated_at
            updated_at_timestamp = item.get('updated_at')
            updated_at = datetime.utcfromtimestamp(updated_at_timestamp)
            print('updated at')
            # contract_date
            contract_date_timestamp = item.get('contract_date')
            contract_date = datetime.utcfromtimestamp(contract_date_timestamp)
            print('updated at')
            # birth_date
            birth_date_timestamp = item.get('birth_date')
            birth_date = datetime.utcfromtimestamp(birth_date_timestamp)
            print('updated at')
            # Foydalanuvchi ma'lumotlarini yangilash
            user = CustomUser.objects.get(employee_id_number=item['employee_id_number'])  # foydalanuvchi obyekti
            user.full_name = item['full_name']
            user.short_name = item['short_name']
            user.first_name = item['first_name']
            user.second_name = item['second_name']
            user.third_name = item['third_name']
            user.gender = gender
            user.birth_date = birth_date
            user.student_id_number = item.get('employee_id_number', '')
            user.full_id = item.get('employee_id_number', '')
            user.gender = gender
            user.academicDegree = academicDegree
            user.academicRank = academicRank
            user.employmentForm = employmentForm
            user.employmentStaff = employmentStaff
            user.staffPosition = staffPosition
            user.employeeStatus = employeeStatus
            user.employeeType = employeeType
            user.department = department
            user.created_at = created_at
            user.updated_at = updated_at
            user.year_of_enter = item.get('year_of_enter', '')
            user.contractDate = contract_date
            user.hash = item.get('hash', '')
            user.is_student = False
            user.is_employee = True
            user.is_active = True
            user.is_followers_book = True
            user.save()

            return JsonResponse({'success': True, 'message': 'Foydalanuvchi ma\'lumotlari yangilandi'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Ma\'lumotlar olishda xatolik'}, status=500)
    except Exception as e:
        print(sys.exc_info())
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


