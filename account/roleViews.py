import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST


def group_list(request):
    groups = Group.objects.all().order_by('-id')  # Id bo'yicha teskari tartibda
    group_data = []

    for group in groups:
        users = [{'initials': user.username} for user in group.user_set.all()]
        group_info = {'id': group.id, 'name': group.name, 'users': users}
        group_data.append(group_info)

    return JsonResponse(group_data, safe=False)



def create_default_groups(request):
    # Grouplarni nomlari
    group_names = ['Student', 'Employee', 'Admin']

    try:
        # Har bir group nomi uchun
        for group_name in group_names:
            # Agar bu nomda guruh mavjud bo'lmasa uni yaratamiz
            if not Group.objects.filter(name=group_name).exists():
                Group.objects.create(name=group_name)
        return JsonResponse({'message': 'Grouplar muvaffaqiyatli yaratildi'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

