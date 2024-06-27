from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@require_POST
@login_required
def change_password(request):
    current_password = request.POST.get('currentPassword')
    new_password = request.POST.get('password')
    new_password_confirm = request.POST.get('password2')

    user = request.user

    if not current_password:
        # Agar current_password bo'sh bo'lsa, yangi parol kiritilishi kerak
        if new_password != new_password_confirm:
            return JsonResponse({'error': 'Yangi parol va tasdiqlash mos kelmayapti'}, status=400)
        else:
            # Yangi parolni kriptografik ravishda saqlash
            new_password = make_password(new_password)
            user.set_password(new_password)
            user.password_save = new_password
            user.save()

            # Foydalanuvchi avtorizatsiyasini yangilash
            user = authenticate(request, username=user.username, password=new_password)
            if user:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Kirish muvaffaqiyatsiz'}, status=400)
    else:
        # Agar current_password mavjud bo'lsa, foydalanuvchi o'zining parolini o'zgartira olishi kerak
        if not user.check_password(current_password):
            return JsonResponse({'error': 'Joriy parol noto\'g\'ri'}, status=400)
        elif new_password != new_password_confirm:
            return JsonResponse({'error': 'Yangi parol va tasdiqlash mos kelmayapti'}, status=400)
        else:
            # Foydalanuvchi parolini o'zgartirish
            user.set_password(new_password)
            user.password_save = new_password
            user.save()

            # Foydalanuvchi avtorizatsiyasini yangilash
            user = authenticate(request, username=user.username, password=new_password)
            if user:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Kirish muvaffaqiyatsiz'}, status=400)
