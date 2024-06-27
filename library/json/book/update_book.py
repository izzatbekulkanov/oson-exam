from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from ...models import Book
import json


def update_book_details(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        # Update book fields with POST data
        book.title = request.POST.get('title', book.title)
        book.authorCode = request.POST.get('authorCode', book.authorCode)
        book.book_type_id = request.POST.get('book_type_id', book.book_type_id)
        book.bbk_id = request.POST.get('bbk_id', book.bbk_id)

        # Set language based on language code
        language_code = request.POST.get('language_id')
        for code, _ in Book.LANGUAGE_CHOICES:
            if code == language_code:
                book.language = code
                break

        # Handle file upload if present
        if 'file' in request.FILES:
            book.file = request.FILES['file']

        # Handle image upload if present
        if 'image' in request.FILES:
            book.image = request.FILES['image']

        # Update authors if provided
        authors = json.loads(request.POST.get('authors', '[]'))
        book.authors.set(authors)  # This sets the book's authors to the provided list, removing any others

        # Save the book instance
        book.save()

        return JsonResponse({'success': True, 'message': 'Kitob muvaffaqiyatli yangilandi'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})