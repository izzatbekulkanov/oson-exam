import json

import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from university.models import University, EducationType, Specialty, Department, EducationForm, Curriculum, \
    EducationLang, GroupUniver
from university.serializers import UniversitySerializer, SpecialtySerializer, CurriculumSerializer, \
    GroupUniverSerializer, DepartmentSerializer


def update_or_create(model, filter_kwargs, defaults=None):
    obj, created = model.objects.get_or_create(**filter_kwargs, defaults=defaults)
    if not created and defaults:
        for key, value in defaults.items():
            setattr(obj, key, value)
        obj.save()
    return obj, created


def update_or_create_department(data):
    department_id = data.get('id')
    name = data.get('name')
    code = data.get('code')
    parent = data.get('parent', None)
    active = data.get('active', False)
    structure_type = data.get('structureType', {}).get('code')

    department, created = Department.objects.update_or_create(
        codeID=department_id,
        defaults={
            'name': name,
            'code': code,
            'parent': parent,
            'active': active,
            'structure_type': structure_type
        }
    )

    # if not created:
    #     print(f"Department '{name}' updated successfully.")
    # else:
    #     print(f"Department '{name}' created successfully.")


def save_university_from_api(request):
    url = 'https://student.namspi.uz/rest/v1/public/university-list?page=20&limit=200'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer cbdfefbb283db3a219a7e7dcefd620b4'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        universities = data.get('data', [])
        for university_data in universities:
            code = university_data.get('code', '')
            name = university_data.get('name', '')
            api_url = university_data.get('api_url', '')
            student_url = university_data.get('student_url', '')
            employee_url = university_data.get('employee_url', '')

            # Check if the university already exists in the database
            existing_university = University.objects.filter(code=code).first()
            if existing_university:
                # Update the existing university
                existing_university.name = name
                existing_university.api_url = api_url
                existing_university.student_url = student_url
                existing_university.employee_url = employee_url
                existing_university.save()
            else:
                # Create a new university
                University.objects.create(
                    code=code,
                    name=name,
                    api_url=api_url,
                    student_url=student_url,
                    employee_url=employee_url
                )

        return HttpResponse("Successfully updated the university list.")
    else:
        return HttpResponse("Failed to update the university list. Status code: {}".format(response.status_code),
                            status=response.status_code)


def save_departments_from_api(request):
    print('adsadsad')
    try:
        # University modelinde is_active alanı True olan bir nesneyi alın
        university = University.objects.get(is_active=True)
        api_url = university.api_url  # API URL'sini alın
        api_token = university.api_token  # API Token'ını alın
        url = f'{api_url}data/department-list?page=20&limit=200'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {api_token}'  # API Token'ını Authorization başlığına ekleyin
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            items = data.get('data', {}).get('items', [])

            for item in items:
                update_or_create_department(item)

            return HttpResponse("Successfully fetched and saved data from the API.")
        else:
            print("Failed to fetch data from the API.")
            return HttpResponse("Failed to fetch data from the API.", status=response.status_code)
    except University.DoesNotExist:
        print("Active university not found.")
        return HttpResponse("Active university not found.", status=404)


def save_specialty_from_api(request):
    try:
        # University modelinde is_active alanı True olan bir nesneyi alın
        university = University.objects.get(is_active=True)
        api_url = university.api_url  # API URL'sini alın
        api_token = university.api_token  # API Token'ını alın
        url = f'{api_url}data/specialty-list?page=20&limit=200'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {api_token}'  # API Token'ını Authorization başlığına ekleyin
        }

        try:

            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Agar status kod 200 bo'lmasa, xato qaytaradi
            data = response.json()
            for item in data.get('data', {}).get('items', []):
                education_type_name = item.get('educationType', {}).get('name')
                education_type_code = item.get('educationType', {}).get('code')
                defaults = {'code': education_type_code}
                obj, created = update_or_create(
                    EducationType,
                    filter_kwargs={'name': education_type_name},
                    defaults=defaults
                )

            # API-dan olingan ma'lumotlarni Speciality modeliga saqlash
            for item in data.get('data', {}).get('items', []):
                # Bo'limni aniqlash
                department_id = item.get('department', {}).get('id')
                department, _ = Department.objects.get_or_create(codeID=department_id)

                # Ta'lim turi ni aniqlash
                education_type_code = item.get('educationType', {}).get('code')
                education_type, _ = EducationType.objects.get_or_create(code=education_type_code)

                # Speciality obyektini yaratish va saqlash
                Specialty.objects.update_or_create(
                    codeID=item.get('id'),
                    defaults={
                        'code': item.get('code'),
                        'name': item.get('name'),
                        'department': department,
                        'educationType': education_type
                    }
                )

            return JsonResponse({'success': True, 'message': 'Ma\'lumotlar muvaffaqiyatli saqlandi'}, status=201)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    except University.DoesNotExist:
        print("Active university not found.")
        return HttpResponse("Active university not found.", status=404)


def save_curriculum_from_api(request):
    try:
        # University modelinde is_active alanı True olan bir nesneyi alın
        university = University.objects.get(is_active=True)
        api_url = university.api_url  # API URL'sini alın
        api_token = university.api_token  # API Token'ını alın
        url = f'{api_url}data/curriculum-list?page=20&limit=200'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {api_token}'  # API Token'ını Authorization başlığına ekleyin
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Agar status kod 200 bo'lmasa, xato qaytaradi
            data = response.json()

            # 'EducationForm' modelini o'zgartirish
            for item in data.get('data', {}).get('items', []):
                education_form_name = item.get('educationForm', {}).get('name')
                education_form_code = item.get('educationForm', {}).get('code')
                EducationForm.objects.get_or_create(
                    name=education_form_name,
                    defaults={'code': education_form_code}
                )

            # 'Curriculum' obyektlarini saqlash
            for item in data.get('data', {}).get('items', []):
                specialty_id = item.get('specialty', {}).get('id')
                specialty, _ = Specialty.objects.get_or_create(codeID=specialty_id)

                education_type_code = item.get('educationType', {}).get('code')
                education_type, _ = EducationType.objects.get_or_create(code=education_type_code)

                education_form_code = item.get('educationForm', {}).get('code')
                education_form = EducationForm.objects.get(code=education_form_code)

                defaults = {
                    'name': item.get('name'),
                    'specialty': specialty,
                    'educationType': education_type,
                    'educationForm': education_form,
                    'semester_count': item.get('semester_count'),
                    'education_period': item.get('education_period'),
                    'codeID': item.get('id'),
                }
                Curriculum.objects.update_or_create(
                    codeID=item.get('id'),
                    defaults=defaults
                )

            return JsonResponse({'success': True, 'message': 'Ma\'lumotlar muvaffaqiyatli saqlandi'}, status=201)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    except University.DoesNotExist:
        print("Active university not found.")
        return HttpResponse("Active university not found.", status=404)


def save_group_from_api(request):
    try:
        # University modelinde is_active alanı True olan bir nesneyi alın
        university = University.objects.get(is_active=True)
        api_url = university.api_url  # API URL'sini alın
        api_token = university.api_token  # API Token'ını alın
        url = f'{api_url}data/group-list'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {api_token}'  # API Token'ını Authorization başlığına ekleyin
        }

        def update_or_create(model, filter_kwargs, defaults=None):
            obj, created = model.objects.get_or_create(**filter_kwargs, defaults=defaults)
            if not created and defaults:
                for key, value in defaults.items():
                    setattr(obj, key, value)
                obj.save()
            return obj, created

        try:
            page_number = 1  # Boshlang'ich sahifa raqami
            while True:
                # Sahifani olish uchun so'rov yaratish
                query_params = {'page': page_number, 'limit': 200}
                response = requests.get(url, headers=headers, params=query_params)
                response.raise_for_status()
                data = response.json()

                # pageCount ni chiqarish
                pagination_data = data.get('data', {}).get('pagination')
                page_count = pagination_data.get('pageCount')

                # Ma'lumotlarni qabul qilish va saqlash
                for item in data.get('data', {}).get('items', []):
                    education_lang_name = item.get('educationLang', {}).get('name')
                    education_lang_code = item.get('educationLang', {}).get('code')
                    defaults = {'code': education_lang_code}
                    obj, created = update_or_create(
                        EducationLang,
                        filter_kwargs={'name': education_lang_name},
                        defaults=defaults
                    )

                    education_lang_code = item.get('educationLang', {}).get('code')
                    education_lang, _ = EducationLang.objects.get_or_create(code=education_lang_code)

                    department_code = item.get('department', {}).get('id')
                    department, _ = Department.objects.get_or_create(codeID=department_code)

                    specialty_id = item.get('specialty', {}).get('id')
                    specialty, _ = Specialty.objects.get_or_create(codeID=specialty_id)

                    GroupUniver.objects.update_or_create(
                        codeID=item.get('id'),
                        defaults={
                            'name': item.get('name'),
                            'educationLang': education_lang,
                            'department': department,
                            'specialty': specialty,
                        }
                    )

                # Keyingi sahifaga o'tish
                if page_number >= page_count:
                    print(page_count)
                    break  # Bo'sh sahifa, dastur to'xtaydi
                else:
                    page_number += 1  # Keyingi sahifaga o'tish

            return JsonResponse({'success': True, 'message': 'Ma\'lumotlar muvaffaqiyatli saqlandi'}, status=201)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    except University.DoesNotExist:
        print("Active university not found.")
        return HttpResponse("Active university not found.", status=404)


def get_universities_data(request):
    search_query = request.GET.get('search', '')
    universities = University.objects.filter(name__icontains=search_query) if search_query else University.objects.all()
    university_serializer = UniversitySerializer(universities, many=True)
    return JsonResponse(university_serializer.data, safe=False)

def get_academic_groups_data(request):
    search_query = request.GET.get('search', '')
    groups = GroupUniver.objects.filter(name__icontains=search_query).order_by('name') if search_query else GroupUniver.objects.all().order_by('name')
    group_serializer = GroupUniverSerializer(groups, many=True)
    return JsonResponse(group_serializer.data, safe=False)

def get_departments_data(request):
    search_query = request.GET.get('search', '')
    departments = Department.objects.filter(name__icontains=search_query) if search_query else Department.objects.all()
    department_serializer = DepartmentSerializer(departments, many=True)
    return JsonResponse(department_serializer.data, safe=False)

def get_specialties_data(request):
    search_query = request.GET.get('search', '')
    specialties = Specialty.objects.filter(name__icontains=search_query) if search_query else Specialty.objects.all()
    specialty_serializer = SpecialtySerializer(specialties, many=True)
    return JsonResponse(specialty_serializer.data, safe=False)

def get_curriculums_data(request):
    search_query = request.GET.get('search', '')
    curriculums = Curriculum.objects.filter(name__icontains=search_query) if search_query else Curriculum.objects.all()
    curriculum_serializer = CurriculumSerializer(curriculums, many=True)
    return JsonResponse(curriculum_serializer.data, safe=False)


def get_universities_with_api_token(request):
    universities_with_token = University.objects.exclude(api_token__isnull=True).exclude(api_token='').order_by('name')
    university_serializer = UniversitySerializer(universities_with_token, many=True)
    return JsonResponse(university_serializer.data, safe=False)

def update_api_token_view(request):
    if request.method == 'POST':
        try:
            # JSON formatidagi malumotlarni olish
            data = json.loads(request.body)

            # Universitet kodini olish
            university_code = data.get('university_code')

            api_token = data.get('api_token')

            # Universitetni bazadan topish
            university = University.objects.get(code=university_code)

            # Universitetni yangilash
            university.api_token = api_token  # Yangi API tokenni saqlash
            university.save()  # O'zgartirishlarni saqlash

            # Muvaffaqiyatli javob qaytarish
            return JsonResponse({'success': True, 'message': 'API token updated successfully'})
        except University.DoesNotExist:
            # Universitet topilmadi xatosi
            return JsonResponse({'success': False, 'message': 'University not found'}, status=404)
        except Exception as e:
            # Boshqa xatoliklar
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        # Noto'g'ri so'rov usuli
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def update_university_status(request):
    if request.method == 'POST':
        university_code = request.POST.get('university_code')
        is_active = request.POST.get('is_active')

        try:
            universities = University.objects.exclude(code=university_code)  # Exclude the current university
            for university in universities:
                university.is_active = False
                university.save()

            # Now update the specific university
            university = University.objects.get(code=university_code)
            university.is_active = True if is_active == 'true' else False  # Convert to boolean
            university.save()

            return JsonResponse({'message': 'University statuses updated successfully.'})
        except University.DoesNotExist:
            return JsonResponse({'error': 'University not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)



def get_departments(request):
    def data_collector(data_list, departments):
        for department in departments:
            data_list.append({
                'name': department.name,
                'code': department.code,
                'structure_type': department.get_structure_type_display(),
                'parent': department.parent if department.parent else '-',
                'is_active': department.active
            })

    fakultet = Department.objects.filter(structure_type=Department.FAKULTET)
    bolim = Department.objects.filter(structure_type=Department.BOLIM)
    kafedra = Department.objects.filter(structure_type=Department.KAFEDRA)
    boshqarma = Department.objects.filter(structure_type=Department.BOSHQARMA)
    markaz = Department.objects.filter(structure_type=Department.MARKAZ)
    rektorat = Department.objects.filter(structure_type=Department.REKTORAT)

    fakultet_data = []
    bolim_data = []
    kafedra_data = []
    boshqarma_data = []
    markaz_data = []
    rektorat_data = []

    data_collector(fakultet_data, fakultet)
    data_collector(bolim_data, bolim)
    data_collector(kafedra_data, kafedra)
    data_collector(boshqarma_data, boshqarma)
    data_collector(markaz_data, markaz)
    data_collector(rektorat_data, rektorat)

    response_data = {
        'fakultet': fakultet_data,
        'bolim': bolim_data,
        'kafedra': kafedra_data,
        'boshqarma': boshqarma_data,
        'markaz': markaz_data,
        'rektorat': rektorat_data,
    }
    return JsonResponse(response_data)