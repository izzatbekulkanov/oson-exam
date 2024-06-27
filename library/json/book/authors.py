from django.http import JsonResponse
from ...models import Author, Book


def authors_list(request):
    if request.method == 'GET':
        search_query = request.GET.get('q', '')
        authors = Author.objects.filter(name__icontains=search_query, is_active=True).values('id', 'name')
        authors_list = list(authors)  # QuerySet-ni list ga o'zgartirish
        return JsonResponse(authors_list, safe=False)

def get_book_authors(request):
    if request.method == 'GET':
        book_id = request.GET.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            authors = book.authors.all().values('id', 'name')
            return JsonResponse({'authors': list(authors)})
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Kitob topilmadi'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)