from django.http import JsonResponse

from account.models import CustomUser
from library.models import Library, Book


def get_statistics(request):
    university = request.user.university
    # Talabalar soni
    students_count = CustomUser.objects.filter(user_type='1', university=university).count()

    # Hodimlar va o'qituvchilar soni
    staff_count = CustomUser.objects.filter(user_type__in=['2', '3'], university=university).count()

    # Kutubhona soni
    libraries_count = Library.objects.filter(university=university).count()

    # Kitoblar soni, universitetga bog'liq kutubxonalar orqali hisoblash
    book_libraries = Library.objects.filter(university=university)
    books_count = Book.objects.filter(library__in=book_libraries).count()

    # Natijalarni JSON formatida qaytarish
    data = {
        'students_count': students_count,
        'staff_count': staff_count,
        'libraries_count': libraries_count,
        'books_count': books_count,
    }

    return JsonResponse(data)