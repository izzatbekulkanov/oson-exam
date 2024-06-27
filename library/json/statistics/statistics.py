from django.http import JsonResponse
from ...models import Library, Book, BookCopy, BookType, BBK, Author
from django.db.models import Count, Prefetch, Q




def library_stats_by_language(request):
    # Tillar ro'yxati
    languages = ['oz', 'ru', 'uz', 'qr', 'all']

    # Bo'sh ma'lumotlar uchun jadval
    data = []

    # Kitob turlarini olish va ular uchun ma'lumotlarni to'plash
    book_types = BookType.objects.prefetch_related('books').all()

    for book_type in book_types:
        # Har bir kitob turi uchun ma'lumotlar
        book_type_data = {
            'name': book_type.name,
            'languages': {}
        }

        # Til bo'yicha ma'lumotlar
        for language in languages:
            if language == 'all':
                # Original kitoblar sonini hisoblash (barcha tillar uchun)
                original_books_count = book_type.books.count()
                # Kitob nusxalari sonini hisoblash (barcha tillar uchun)
                book_copies_count = BookCopy.objects.filter(original_book__book_type=book_type).count()
            else:
                # Original kitoblar sonini hisoblash
                original_books_count = book_type.books.filter(language=language).count()

                # Kitob nusxalari sonini hisoblash
                book_copies_count = BookCopy.objects.filter(original_book__book_type=book_type, original_book__language=language).count()

            # Til bo'yicha ma'lumotlar qo'shish
            book_type_data['languages'][language] = {
                'original_books_count': original_books_count,
                'book_copies_count': book_copies_count
            }

        # Jami ma'lumotlar qismi
        total_original_books = sum(lang['original_books_count'] for lang in book_type_data['languages'].values())
        total_book_copies = sum(lang['book_copies_count'] for lang in book_type_data['languages'].values())

        book_type_data['total_original_books'] = total_original_books
        book_type_data['total_book_copies'] = total_book_copies

        data.append(book_type_data)

    # JSON javobi
    response_data = {
        'languages': languages,
        'data': data
    }

    return JsonResponse(response_data)