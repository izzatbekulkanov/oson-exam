from django.http import JsonResponse
from ...models import Book, BookCopy


def get_book_details(request):
    if request.method == 'GET':
        book_id = request.GET.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            copies = BookCopy.objects.filter(original_book=book)
            copy_data = []
            for copy in copies:
                copy_data.append({
                    'id': copy.id,
                    'inventory_number': copy.inventory_number,
                    'status': copy.status,
                    'library': copy.library.name if copy.library else None,
                    'haveStatus': 'Mavjud' if copy.haveStatus == 'yes' else 'Band kitob',
                    'accepted_by': copy.accepted_by.username if copy.accepted_by else None,
                    'send_date': copy.send_date.strftime('%Y-%m-%d %H:%M') if copy.send_date else None,
                    'accept_date': copy.accept_date.strftime('%Y-%m-%d %H:%M') if copy.accept_date else None,
                    'created_at': copy.created_at.strftime('%Y-%m-%d %H:%M'),
                    'updated_at': copy.updated_at.strftime('%Y-%m-%d %H:%M'),
                })
            book_data = {
                'id': book.id,
                'title': book.title,
                'authors': ', '.join([author.name for author in book.authors.all()]),
                'author_code': book.authorCode,
                'quantity': book.quantity,
                'adad': book.adad,
                'image': book.image.url if book.image else None,
                'library': book.library.name if book.library else None,
                'status': book.status,
                'added_by': book.added_by.username if book.added_by else None,
                'isbn': book.isbn,
                'file': book.file.url if book.file else None,
                'book_type': book.book_type.name if book.book_type else None,
                'book_type_id': book.book_type.id if book.book_type else None,
                'bbk': book.bbk.name if book.bbk else None,
                'bbk_code': book.bbk.code if book.bbk else None,
                'bbk_id': book.bbk.id if book.bbk else None,
                'is_online': book.is_online,
                'language': dict(Book.LANGUAGE_CHOICES).get(book.language),
                'language_id': book.language,
                'publication_year': book.publication_year,
                'publisher': book.publisher,
                'published_city': book.published_city,
                'annotation': book.annotation,
                'pages': book.pages,
                'created_at': book.created_at.strftime('%Y-%m-%d %H:%M'),
                'updated_at': book.updated_at.strftime('%Y-%m-%d %H:%M'),
                'copies': copy_data,
            }
            return JsonResponse(book_data)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Kitob topilmadi'}, status=404)
    else:
        return JsonResponse({'error': 'Faqat AJAX so\'rovlarni qabul qilinadi'}, status=400)