from django.utils import timezone
from django.db.models import Count

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from ...models import Book, BookCopy, Library


def get_books_by_book_type_and_bbk(request):
    book_type_id = request.GET.get('book_type_id')
    bbk_id = request.GET.get('bbk_id')

    if book_type_id and bbk_id:
        try:
            # Tanlangan book_type_id va bbk_id bo'yicha kitoblarni olish
            books = Book.objects.filter(book_type_id=book_type_id, bbk_id=bbk_id)
            book_list = serialize_books(books)

            return JsonResponse({'books': book_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'book_type_id yoki bbk_id parameterlari jo\'natilmadi'}, status=400)


def serialize_books(books):
    serialized_books = []
    for book in books:
        serialized_book = {
            'title': book.title,
            'language': book.language,
            'id': book.id,
            'isbn': book.isbn,
            # Qo'shimcha maydonlarni ham qo'shing
        }
        serialized_books.append(serialized_book)
    return serialized_books


@csrf_exempt  # Use csrf_exempt if you are not sending CSRF token from the frontend (not recommended for production)
@require_POST
def select_book_copy(request):
    book_id = request.POST.get('book_id')
    if book_id:
        try:
            book_copies = BookCopy.objects.filter(original_book_id=book_id, status='not_accepted')
            book_copy_list = serialize_book_copies(book_copies)
            return JsonResponse({'book_copies': book_copy_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'book_id parameteri topilmadi'}, status=400)


def serialize_book_copies(book_copies):
    serialized_book_copies = []
    for book_copy in book_copies:
        serialized_book_copy = {
            'id': book_copy.id,
            'title': book_copy.original_book.title,  # Access the title through the original book
            'language': book_copy.original_book.language,  # Access the title through the original book
            'created_at': book_copy.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format the datetime if needed
            'inventory_number': book_copy.inventory_number,
            'status': book_copy.status,
            # Add other fields if necessary
        }
        serialized_book_copies.append(serialized_book_copy)
    return serialized_book_copies


@login_required  # Ensure the user is logged in
def get_user_libraries(request):
    user = request.user

    # Get libraries where the user is the big librarian
    libraries = Library.objects.filter(big_librarian=user)

    if libraries.exists():
        # Serialize the libraries
        libraries_list = [{
            'id': library.id,
            'name': library.name,
            'address': library.address,
            'number': library.number,
            'university': library.university.name if library.university else None,
            'created_date': library.created_date.strftime('%Y-%m-%d'),
            'updated_date': library.updated_date.strftime('%Y-%m-%d'),
            'user': library.user.username,
            'active': library.active,
        } for library in libraries]

        return JsonResponse({'libraries': libraries_list})
    else:
        return JsonResponse({'message': 'Hech qanday libraryga birikmagan'}, status=404)


@login_required
@csrf_exempt
def assign_book_copies_to_library(request):
    if request.method == 'POST':
        library_id = request.POST.get('library_id')
        book_copy_ids = request.POST.getlist('book_copy_ids[]')

        if not library_id or not book_copy_ids:
            return JsonResponse({'error': 'Kutubxona ID yoki kitob nusxalari IDlari berilmagan'}, status=400)

        try:
            library = Library.objects.get(id=library_id)
        except Library.DoesNotExist:
            return JsonResponse({'error': 'Kutubxona topilmadi'}, status=404)

        try:
            book_copies = BookCopy.objects.filter(id__in=book_copy_ids)
            now_date = timezone.now()

            # Kitob nusxalarini yangilash
            book_copies.update(library=library, status='sent', send_date=now_date)

            # Tegishli original kitoblarni topish va statuslarini yangilash
            original_books = Book.objects.filter(copies__in=book_copies).distinct()
            original_books.update(status='distributed')

            return JsonResponse({'message': 'Kitob nusxalari muvaffaqiyatli biriktirildi'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Faqat POST so\'rovi qabul qilinadi'}, status=405)



def get_not_accepted_book_copies(request):
    # BBK va BookType bo'yicha not_accepted statusiga ega kitob nusxalarini guruhlash va hisoblash
    result = BookCopy.objects.filter(status='not_accepted').values(
        'id',
        'original_book__id',
        'original_book__title',
        'original_book__bbk__name',
        'original_book__book_type__name',
        'status',
        'created_at',
        'original_book__created_at'
    )

    # Natijani JSON formatiga o'tkazish
    data = {}
    for entry in result:
        bbk_name = entry['original_book__bbk__name']
        book_type_name = entry['original_book__book_type__name']
        book_copy_id = entry['id']
        book_status = entry['status']
        book_title = entry['original_book__title']
        created_at = entry['created_at']
        original_book_created_at = entry['original_book__created_at']
        original_book_id = entry['original_book__id']

        # Agar BBK nomi mavjud bo'lmasa, yangi lug'at qo'shish
        if bbk_name not in data:
            data[bbk_name] = {}

        # Agar kitob turi mavjud bo'lmasa, yangi lug'at qo'shish
        if book_type_name not in data[bbk_name]:
            data[bbk_name][book_type_name] = []

        # Har bir kitob nusxasi uchun ma'lumotlarni qo'shish
        data[bbk_name][book_type_name].append({
            'book_copy_id': book_copy_id,
            'book_title': book_title,
            'status': book_status,
            'book_copy_created_at': created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'original_book_created_at': original_book_created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'original_book_id': original_book_id
        })

    return JsonResponse(data)
