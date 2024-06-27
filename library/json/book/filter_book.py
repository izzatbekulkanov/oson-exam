from django.shortcuts import render
from django.http import JsonResponse
from library.models import Book

def filter_books(request):
    book_type = request.GET.get('book_type', None)
    bbk = request.GET.get('bbk', None)
    status = request.GET.get('status', None)
    file = request.GET.get('file', None)

    # 'Tanlang' yoki bo'sh satr bo'lsa, None ga o'zgartiramiz
    if not book_type or book_type == 'Tanlang':
        book_type = None

    if not bbk or bbk == 'Tanlang':
        bbk = None

    books = Book.objects.all()

    if book_type is not None:
        books = books.filter(book_type__id=book_type)

    if bbk is not None:
        books = books.filter(bbk__id=bbk)

    if status:
        books = books.filter(status=status)

    if file:
        if file == 'ha':
            books = books.exclude(file__isnull=True)
        elif file == 'yoq':
            books = books.filter(file__isnull=True)

    # Saralashni qo'llash
    books = books.order_by('title')

    books_data = [
        {
            'id': book.id,
            'language': book.language,
            'title': book.title,
            'book_type': book.book_type.name if book.book_type else '',
            'bbk': f"{book.bbk.code} | {book.bbk.name}" if book.bbk else '',
            'authors': ", ".join([author.name for author in book.authors.all()]),
            'authors_code': book.authorCode,
            'file': book.file.url if book.file else '',
            'status': book.status,
            'created_at': book.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'quantity': book.quantity,  # Kitob nusxalari soni
            'copy_count': book.copies.count()  # Kitob nusxalari soni (BookCopy modeli orqali)
        }
        for book in books
    ]

    return JsonResponse({'books': books_data})