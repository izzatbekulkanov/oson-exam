from django.http import JsonResponse

from library.models import Library


def libraries_list(request):
    if request.user.groups.filter(name='Administrator').exists():
        libraries = Library.objects.all().order_by('-id')
    else:
        user_university = request.user.university
        libraries = Library.objects.filter(university=user_university).order_by('-id')

    data = []

    for library in libraries:
        librarian_data = []
        for librarian in library.small_librarians.all():
            librarian_info = {
                'username': librarian.username,
                'full_name': librarian.full_name,
                'email': librarian.email,
                'id': librarian.id,
            }
            librarian_data.append(librarian_info)

        admin_librarian_data = None
        if library.big_librarian:
            admin_librarian_data = {
                'username': library.big_librarian.username,
                'full_name': library.big_librarian.full_name,
                'id': library.big_librarian.id,
            }

        # Avtorlar sonini hisoblash
        book_authors_count = 0
        for book in library.books.all():
            book_authors_count += book.authors.count()

        library_data = {
            'id': library.id,
            'name': library.name,
            'address': library.address,
            'university': library.university.name if library.university else None,
            'book_count': library.books.count(),
            'author_count': book_authors_count,
            'admin': admin_librarian_data,
            'small_admins': librarian_data if librarian_data else None,
            'small_librarians_count': library.small_librarians.count() if librarian_data else 0,
            'active': library.active,
            'action': True if admin_librarian_data or librarian_data else False,
        }

        data.append(library_data)

    return JsonResponse(data, safe=False)