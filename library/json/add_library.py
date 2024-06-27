import json

from django.contrib.auth.models import Group
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from account.models import CustomUser
from library.models import Library
from university.models import University


# Kutubhona yaratish
def create_library_json(request):
    if request.method == 'POST':
        # Foydalanuvchi obyektini olish
        user = request.user
        json_data = json.loads(request.body)

        # POST so'rov orqali kutubhona ma'lumotlarini olish
        name = json_data.get('name')
        address = json_data.get('address')
        number = json_data.get('number')
        university_code = json_data.get('university_code')

        # Universitetni tekshirish
        try:
            university = University.objects.get(code=university_code)
        except University.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Berilgan kodli universitet topilmadi'}, status=404)

        # `'`, `"`, yoki ` belgilari to'g'risidagi kodlar
        name = name.replace("'", "").replace('"', "").replace("`", "")
        address = address.replace("'", "").replace('"', "").replace("`", "")
        number = number.replace("'", "").replace('"', "").replace("`", "")

        # Yangi kutubhona obyektini yaratish
        new_library = Library(name=name, address=address, number=number, user=user, active=True, university=university)
        new_library.save()

        # Kutubhonani muvaffaqiyatli yaratilgandan keyin foydalanuvchini profiliga yo'naltirish
        return JsonResponse({'success': True, 'message': 'Kutubhona muvaffaqiyatli saqlandi'}, status=200)


def get_librarians_per_university(request):
    # Aktiv universitetlarni olish
    active_universities = University.objects.filter(is_active=True)

    # Har bir universitet uchun kutubhonalardagi small_librarianlar sonini va big_librarian obyektini hisoblash
    university_data = []
    for university in active_universities:
        # Kutubhonalar ro'yxatini olish
        libraries = university.libraries.all()

        # Kutubhonalardagi small_librarianlar sonini hisoblash
        small_librarian_count = libraries.aggregate(total=Count('small_librarians'))['total']

        # Big_librarian obyektini olish
        big_librarian = None
        for library in libraries:
            if library.big_librarian:
                big_librarian = library.big_librarian
                break

        # Universitetning ma'lumotlari
        university_info = {
            'university_name': university.name,
            'university_code': university.code,
            'library_count': libraries.count(),  # Universitetga birikkan kutubxonalar soni
            'small_librarian_count': small_librarian_count,
            'big_librarian': {
                'full_name': big_librarian.full_name if big_librarian else "Kutubhona rahbari yoq",
                'email': big_librarian.email if big_librarian else None,
            } if big_librarian else None
        }
        university_data.append(university_info)

    # JSON javobini qaytarish
    return JsonResponse({'universities': university_data})


def get_library_admins(request):
    # LibraryAdmin guruhini olish
    try:
        library_admin_group = Group.objects.get(name='LibraryAdmin')
    except Group.DoesNotExist:
        return JsonResponse({'error': 'LibraryAdmin group not found'}, status=404)

    # Guruhga azo bo'lgan foydalanuvchilarni olish
    library_admins = library_admin_group.user_set.all()

    # Foydalanuvchilar ma'lumotlarini yig'ish
    admins_data = []
    for admin in library_admins:
        admin_info = {
            'id': admin.id,
            'username': admin.username,
            'email': admin.email,
            'first_name': admin.first_name.title() if admin.first_name else None,
            'second_name': admin.second_name.title() if admin.second_name else None,
            'third_name': admin.third_name.title() if admin.third_name else None,
            'full_name': admin.full_name.title() if admin.full_name else None,
            # Boshqa kerakli ma'lumotlarni ham qo'shishingiz mumkin
        }
        admins_data.append(admin_info)

    # JSON javobini qaytarish
    return JsonResponse({'library_admins': admins_data})


def assign_big_librarian(request):
    if request.method == 'POST':
        university_code = request.POST.get('university_code')
        big_librarian_id = request.POST.get('big_librarian_id')

        university = get_object_or_404(University, code=university_code)
        big_librarian = get_object_or_404(CustomUser, id=big_librarian_id)

        libraries = university.libraries.all()
        for library in libraries:
            library.big_librarian = big_librarian
            library.save()

        return JsonResponse({'success': 'Big librarian assigned successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_small_librarians(request):
    try:
        library_admin_group = Group.objects.get(name='Library')
    except Group.DoesNotExist:
        return JsonResponse({'error': 'LibraryAdmin group not found'}, status=404)

    # Guruhga azo bo'lgan foydalanuvchilarni olish
    library_admins = library_admin_group.user_set.all()

    selected_library_id = request.GET.get('library_id')
    selected_library = get_object_or_404(Library, id=selected_library_id)

    # Foydalanuvchilar ma'lumotlarini yig'ish
    admins_data = []
    for admin in library_admins:
        admin_info = {
            'id': admin.id,
            'username': admin.username,
            'email': admin.email,
            'first_name': admin.first_name.title() if admin.first_name else None,
            'second_name': admin.second_name.title() if admin.second_name else None,
            'third_name': admin.third_name.title() if admin.third_name else None,
            'full_name': admin.full_name.title() if admin.full_name else None,
            'selected': admin in selected_library.small_librarians.all()
            # Boshqa kerakli ma'lumotlarni ham qo'shishingiz mumkin
        }
        admins_data.append(admin_info)

    # JSON javobini qaytarish
    return JsonResponse({'library_admins': admins_data})


def assign_small_librarian(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        library_id = data.get('library_id')
        small_librarian_ids = data.get('small_librarian_id')  # Barcha tanlangan foydalanuvchilar idsi

        print(library_id, small_librarian_ids)

        library = get_object_or_404(Library, id=library_id)

        # Oldingi small librariansni o'chirish
        library.small_librarians.clear()

        # Har bir small_librarian_id uchun biriktirish
        for small_librarian_id in small_librarian_ids:
            small_librarian = get_object_or_404(CustomUser, id=small_librarian_id)

            # Oldingi kutubxonalardan olib tashlash
            for previous_library in small_librarian.small_librarian_libraries.all():
                previous_library.small_librarians.remove(small_librarian)

            # Yangi kutubxonaga qo'shish
            library.small_librarians.add(small_librarian)

        library.save()

        return JsonResponse({'success': 'Small librarians assigned successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
