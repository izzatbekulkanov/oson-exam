import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.views.decorators.http import require_POST


def group_list(request):
    groups = Group.objects.all().order_by('-id')  # Id bo'yicha teskari tartibda
    group_data = []

    for group in groups:
        users = [{'initials': user.username} for user in group.user_set.all()]
        group_info = {'id': group.id, 'name': group.name, 'users': users}
        group_data.append(group_info)

    return JsonResponse(group_data, safe=False)


def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            group = Group.objects.create(name=name)
            return JsonResponse({'success': 'Group created successfully', 'id': group.id})
        else:
            return JsonResponse({'error': 'Name field is required'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


def create_default_groups(request):
    # Grouplarni nomlari
    group_names = ['Library', 'LibraryAdmin', 'Administrator', 'RTTM', 'Student', 'Employee']

    try:
        # Har bir group nomi uchun
        for group_name in group_names:
            # Agar bu nomda guruh mavjud bo'lmasa uni yaratamiz
            if not Group.objects.filter(name=group_name).exists():
                Group.objects.create(name=group_name)
        return JsonResponse({'message': 'Grouplar muvaffaqiyatli yaratildi'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_user_groups(request):
    user = request.user
    groups = user.groups.all()

    # Serialize the groups
    groups_list = [{'id': group.id, 'name': group.name} for group in groups]

    return JsonResponse({'groups': groups_list, 'now_role': user.now_role})


@require_POST
@login_required
def set_now_role(request):
    try:
        data = json.loads(request.body)
        group_name = data.get('now_role')

        if group_name:
            # Assuming you have a CustomUser model with a field named now_role
            request.user.now_role = group_name
            request.user.save()

            return JsonResponse({'status': 'success'})

    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON data')

    return HttpResponseBadRequest('Bad request')
