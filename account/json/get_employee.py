from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.utils.dateformat import format
from ..models import CustomUser


def format_datetime(dt):
    # Datetime formatini "Y-m-d H:i" ko'rinishida formatlash
    return format(dt, 'Y-m-d H:i')


def get_employee_users(request):
    # Hodim bo'lgan foydalanuvchilarni olish va bog'liq obyektlarni oldindan yuklab olish
    employee_users = CustomUser.objects.filter(is_employee=True).select_related(
        'department', 'staffPosition', 'curriculum', 'specialty', 'university'
    )

    # Faqat kerakli ustunlarni (fields) tanlang
    fields = ['full_name', 'image', 'imageFile', 'birth_date', 'department', 'staffPosition', 'full_id',
              'now_role', 'created_at', 'updated_at', 'curriculum', 'specialty', 'is_active', 'university', 'id']

    # Hodim bo'lgan foydalanuvchilarni qayta ishlash
    employee_users_data = []
    for user in employee_users:
        user_data = {}
        for field in fields:
            if field in ['created_at', 'updated_at']:
                user_data[field] = format_datetime(getattr(user, field))
            elif field in ['department', 'staffPosition', 'curriculum', 'specialty', 'university']:
                related_object = getattr(user, field)
                user_data[field + '_name'] = related_object.name if related_object else None
            elif field == 'imageFile':
                user_data[field] = user.imageFile.url if user.imageFile else None
            else:
                user_data[field] = getattr(user, field)
        employee_users_data.append(user_data)

    return JsonResponse(employee_users_data, safe=False)


def get_employee_details(request, id):
    # Ma'lumotlar bazasidan foydalanuvchi obyektini olish
    employee = get_object_or_404(CustomUser, id=id)

    # Guruhlarni olish
    all_groups = Group.objects.all()

    # Foydalanuvchi a'zo bo'lgan guruhlarni olish
    user_groups = employee.groups.all()

    # Guruhlarni ro'yxatini tayyorlash
    groups_list = [{'id': group.id, 'name': group.name, 'selected': group in user_groups} for group in all_groups]

    # Foydalanuvchi obyektiga guruhlar ro'yxatini qo'shish
    employee_data = {
        'id': employee.id,
        'full_name': employee.full_name,
        'short_name': employee.short_name,
        'first_name': employee.first_name,
        'second_name': employee.second_name,
        'third_name': employee.third_name,
        'gender': employee.gender.name if employee.gender else None,
        'university': employee.university.name if employee.university else "Universitetga birikmagan",
        'birth_date': employee.birth_date,
        'student_id_number': employee.student_id_number,
        'image_url': employee.image if employee.image else None,
        'image_file_url': employee.imageFile.url if employee.imageFile else None,
        'country': employee.country.name if employee.country else None,
        'address': employee.address if employee.address else 'Mavjud emas',
        'province': employee.province.name if employee.province else 'Mavjud emas',
        'district': employee.district.name if employee.district else 'Mavjud emas',
        'citizenship': employee.citizenship.name if employee.citizenship else None,
        'student_status': employee.studentStatus.name if employee.studentStatus else None,
        'email': employee.email,
        'username': employee.username,
        'curriculum': employee.curriculum if employee.curriculum else None,
        # 'department': employee.department if employee.department.name else None,
        'academic_degree': employee.academicDegree if employee.academicDegree else None,
        'academic_rank': employee.academikRank if employee.academikRank else None,
        'employment_form': employee.employmentForm if employee.employmentForm else None,
        'employment_staff': employee.employmentStaff if employee.employmentStaff else None,
        'employment_status': employee.employeeStatus if employee.employeeStatus else None,
        'staff_position': employee.staffPosition if employee.staffPosition else None,
        'payment_form': employee.paymentForm if employee.paymentForm else None,
        'user_type': employee.get_user_type_display(),
        'roles': [role.name for role in employee.hemis_role.all()],
        'employee_type': employee.employeeType if employee.employeeType else None,
        'is_student': employee.is_student,
        'is_employee': employee.is_employee,
        'is_followers_book': employee.is_followers_book,
        'last_login': employee.last_login,
        'last_activity': employee.last_activity,
        'is_staff': employee.is_staff,
        'is_active': employee.is_active,
        'token': employee.token,
        'passport_serial': employee.passport_serial,
        'passport_issue_date': employee.passport_issue_date,
        'passport_jshshir': employee.passport_jshshir,
        'full_id': employee.full_id,
        'telegram': employee.telegram if employee.telegram else 'Telegram foydalanuvchi nomingizni kiriting',
        'instagram': employee.instagram if employee.instagram else 'Instagram foydalanuvchi nomingizni kiriting',
        'facebook': employee.facebook if employee.facebook else 'Facebook foydalanuvchi nomingizni kiriting',
        'created_at': employee.created_at,
        'updated_at': employee.updated_at,
        'groups': groups_list,
    }

    return render(request, 'applications/account/employee/detailEmployee.html', {'employee_data': employee_data})


def update_employee_profile_from_api(request):
    # Foydalanuvchi ID sini HTML formasi orqali qabul qilish
    id = request.POST.get('id')

    # Foydalanuvchini bazadan olish
    employee = get_object_or_404(CustomUser, pk=id)

    # Barcha guruhlarni bazadan olish
    all_groups = Group.objects.all()

    # Foydalanuvchining guruhlarini olish
    user_groups = employee.groups.all()

    # Guruhlarni JSON formatida tayyorlash
    groups_list = [{'id': group.id, 'name': group.name, 'selected': group in user_groups} for group in all_groups]

    # JSON formatida javob qaytarish
    return JsonResponse({'id': id, 'groups': groups_list})


def save_employee_groups(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        selected_group_ids = request.POST.getlist('groups[]')

        # Foydalanuvchi obyektini topish
        employee = CustomUser.objects.get(id=employee_id)

        # Tanlangan guruhlarni ajratish
        selected_groups = Group.objects.filter(id__in=selected_group_ids)

        # Foydalanuvchining barcha guruhlari
        all_user_groups = employee.groups.all()

        # Foydalanuvchi rolini tekshirish
        if not request.user.groups.filter(name__in=['Administrator', 'RTTM']).exists():
            return JsonResponse({'success': False, 'message': 'Sizda bunday huquq yo\'q'}, status=403)

        # Tanlangan guruhlarni azo qilish
        for group in selected_groups:
            employee.groups.add(group)

        # Tanlanmagan guruhlarni olib tashlash
        unselected_groups = all_user_groups.exclude(id__in=selected_group_ids)
        for group in unselected_groups:
            employee.groups.remove(group)

        # Barcha guruhlar ro'yxatini olish
        all_groups = Group.objects.all()

        # Guruhlar ro'yxatini JSON formatiga tayyorlash
        groups_list = [{'id': group.id, 'name': group.name, 'selected': group in selected_groups} for group in
                       all_groups]

        return JsonResponse({'success': True, 'message': 'Guruhlar saqlandi', 'groups': groups_list})
    else:
        return JsonResponse({'success': False, 'message': 'Not allowed'}, status=405)
