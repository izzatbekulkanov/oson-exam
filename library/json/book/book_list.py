from django.http import JsonResponse

from ...models import Book, BookType


def get_recently_added_books(request):
    # O'zgaruvchini asosiy kitoblar ro'yhatini oluvchi so'rovni yaratish
    recently_added_books = Book.objects.all().order_by('-created_at')[:10]

    # JSON javob uchun kitoblar ro'yhatini tayyorlash
    books_list = []
    for book in recently_added_books:
        book_data = {
            'title': book.title,
            'author': ', '.join([author.name for author in book.authors.all()]),
            'quantity': book.quantity,
            'isbn': book.isbn,
            'publication_year': book.publication_year,
            'publisher': book.publisher,
            'status': book.status,
            'created_at': book.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'annotation': book.annotation,
            'pages': book.pages,
            'language': book.language,
            'image': book.image.url if book.image else None,
            'file': book.file.url if book.file else None,
        }
        books_list.append(book_data)

    # JSON javobni qaytarish
    return JsonResponse({'recently_added_books': books_list})


def get_book_types(request):
    # BookType obyektlarini olish
    book_types = BookType.objects.all()

    # JSON javob uchun book type ro'yhatini tayyorlash
    book_types_list = []
    for book_type in book_types:
        book_type_data = {
            'id': book_type.id,
            'name': book_type.name,
            'image': book_type.image.url if book_type.image else None,
            'created_at': book_type.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': book_type.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': book_type.is_active,
            'user': book_type.user.id if book_type.user else None,
        }
        book_types_list.append(book_type_data)

    # JSON javobni qaytarish
    return JsonResponse({'book_types': book_types_list})





