from django.http import JsonResponse
from django.utils.dateformat import format
from ..models import CustomUser


def format_datetime(dt):
    # Datetime formatini "Y-m-d H:i" ko'rinishida formatlash
    return format(dt, 'Y-m-d H:i')


def get_student_users(request):
    # Hodim bo'lgan foydalanuvchilarni olish va bog'liq obyektlarni oldindan yuklab olish
    employee_users = CustomUser.objects.filter(is_student=True).select_related(
        'department', 'curriculum', 'specialty', 'university', 'group', 'level'
    )

    # Faqat kerakli ustunlarni (fields) tanlang
    fields = ['full_name', 'image', 'imageFile', 'birth_date', 'department', 'level', 'full_id',
              'now_role', 'created_at', 'updated_at', 'curriculum', 'specialty', 'is_active', 'university', 'group', 'id']

    # Hodim bo'lgan foydalanuvchilarni qayta ishlash
    employee_users_data = []
    for user in employee_users:
        user_data = {}
        for field in fields:
            if field in ['created_at', 'updated_at']:
                user_data[field] = format_datetime(getattr(user, field))
            elif field in ['department', 'group', 'curriculum', 'specialty', 'university', 'level']:
                related_object = getattr(user, field)
                user_data[field + '_name'] = related_object.name if related_object else None
            elif field == 'imageFile':
                user_data[field] = user.imageFile.url if user.imageFile else None
            else:
                user_data[field] = getattr(user, field)
        employee_users_data.append(user_data)

    return JsonResponse(employee_users_data, safe=False)
