from django.http import JsonResponse
from django.views.decorators.http import require_POST

from university.models import University
from ...models import CustomUser  # O'zgartiring
from django.contrib.auth import login, authenticate


@require_POST
def create_employee(request):
    # Ma'lumotlarni qabul qilish
    username = request.POST.get('validationCustom01')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('second_name')
    email = request.POST.get('email')
    university_id = request.POST.get('employeeUniversity')
    # university_id orqali universitet obyektini olish mumkin
    university = University.objects.get(code=university_id)  # O'zgartiring

    # Yaratilayotgan foydalanuvchi obyektini saqlash
    employee = CustomUser.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_employee=True,
        university=university,
        password_save=password
    )

    # Foydalanuvchi email va parol bilan tizimga kirish
    user = authenticate(request, email=email, password=password)
    if user is not None:
        pass
    else:
        # Foydalanuvchi ma'lumotlari to'g'ri kelmadi
        # Ma'lumotlarni qayta tekshirish yoki xatolik haqida xabar berish mumkin
        pass

    # Uyali javob
    return JsonResponse({'success': True, 'message': 'Yangi foydalanuvchi muvaffaqiyatli yaratildi va tizimga kirdi.'})
