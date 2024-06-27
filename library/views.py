from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import BookLoan, BookOrder, BookType, BBK, Book
from datetime import datetime


@login_required
def library_dashboard(request):
    if request.user.is_authenticated:
        if request.user.now_role in ['Library', 'Administrator']:
            try:
                return render(request, 'app/library/index.html')
            except request.user.DoesNotExist:
                pass  # Hata durumunda aşağıdaki kısımda kullanıcıyı yönlendireceğiz

        # "Library" veya "Administrator" grubuna üye olmayan kullanıcılar için
        return redirect('error')  # Hata URL'sine yönlendirme
    else:
        # Oturum açmamış kullanıcılar için
        return redirect('login')  # Giriş URL'sine yönlendirme


@login_required
def library_views(request):
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'LibraryAdmin'] and request.user.groups.filter(
                    name__in=['Administrator', 'Library']).exists():
                breadcrumb = {
                    'parent': 'Kutubxona',  # Ota-ona sahifa nomi
                    'child': 'Kutubxonalar ro\'yhati'  # Hozirgi sahifa nomi
                }
                return render(request, 'applications/library/libraryList/libraryList.html', {'breadcrumb': breadcrumb})
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')


@login_required
def library_admin_views(request):
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'LibraryAdmin'] and request.user.groups.filter(
                    name__in=['Administrator', 'LibraryAdmin']).exists():
                breadcrumb = {
                    'parent': 'Kutubxona',  # Ota-ona sahifa nomi
                    'child': 'Kutubxonalar hodimlari'  # Hozirgi sahifa nomi
                }
                return render(request, 'applications/library/librarian/librarian.html', {'breadcrumb': breadcrumb})
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')


@login_required
def book_list(request):
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'Library', 'LibraryAdmin']:
                if request.user.groups.filter(name__in=['Administrator', 'Library', 'LibraryAdmin']).exists():
                    breadcrumb = {
                        'parent': 'Kutubxona',  # Ota-ona sahifa nomi
                        'child': 'Kitoblar ro\'yhati'  # Hozirgi sahifa nomi
                    }
                    return render(request, 'applications/library/book/book-list.html', {'breadcrumb': breadcrumb})
                else:
                    return redirect('index')
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')


@login_required
def book_bbk_list(request):
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'Library', 'LibraryAdmin']:
                if request.user.groups.filter(name__in=['Administrator', 'Library', 'LibraryAdmin']).exists():
                    book_type_id = request.GET.get('type')
                    # Kitoblar ro'yxati berilgan book type bo'yicha filtrlanadi
                    books = Book.objects.filter(book_type_id=book_type_id)
                    book_type = get_object_or_404(BookType, id=book_type_id)

                    # Bu kitoblarning biriktirilgan BBKlar ro'yxatini olish
                    bbks = BBK.objects.filter(books_bbk__in=books).distinct()

                    breadcrumb = {
                        'parent': 'Kutubxona',  # Ota-ona sahifa nomi
                        'child': 'BBK Kitoblar ro\'yhati'  # Hozirgi sahifa nomi
                    }

                    context = {
                        'book_type': book_type,
                        'bbks': bbks,
                        'breadcrumb': breadcrumb  # breadcrumb'ni contextga qo'shish
                    }
                    return render(request, 'applications/library/book/bbk-book-list.html', context)
                else:
                    return redirect('index')
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')


@login_required
def all_book_list(request):
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'Library', 'LibraryAdmin']:
                if request.user.groups.filter(name__in=['Administrator', 'Library', 'LibraryAdmin']).exists():
                    bbk_id = request.GET.get('bbk')
                    if bbk_id:
                        bbk = get_object_or_404(BBK, id=bbk_id)
                        books = Book.objects.filter(bbk=bbk, status='distributed')
                    else:
                        books = Book.objects.none()

                    breadcrumb = {
                        'parent': 'Kutubxona',  # Ota-ona sayfa adı
                        'child': 'Barcha Kitoblar'  # Mevcut sayfa adı
                    }

                    context = {
                        'books': books,
                        'bbk': bbk,
                        'breadcrumb': breadcrumb  # breadcrumb'ı context'e ekleme
                    }
                    return render(request, 'applications/library/book/all-book-list.html', context)
                else:
                    return redirect('index')
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')

@login_required
def book_category(request):
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'LibraryAdmin'] and request.user.groups.filter(
                    name__in=['Administrator', 'LibraryAdmin']).exists():
                breadcrumb = {
                    'parent': 'Kutubxona',  # Ota-ona sayfa adı
                    'child': 'Kitob Kategoriyalari'  # Mevcut sayfa adı
                }
                return render(request, 'applications/library/category/category.html', {'breadcrumb': breadcrumb})
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')


@login_required
def book_author_view(request):
    """Kitob mualliflari sahifasi."""
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'Library', 'LibraryAdmin'] and request.user.groups.filter(
                    name__in=['Administrator', 'LibraryAdmin']).exists():
                breadcrumb = {
                    'parent': 'Kutubxona',  # Ota-ona sayfa adı
                    'child': 'Kitob Mualliflari'  # Mevcut sayfa adı
                }
                return render(request, 'app/library/pages/authors.html', {'breadcrumb': breadcrumb})
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')


@login_required
def add_book_view(request):
    """Yangi kitob qo'shish."""
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'LibraryAdmin'] and request.user.groups.filter(
                    name__in=['Administrator', 'LibraryAdmin']).exists():
                breadcrumb = {
                    'parent': 'Kutubxona',  # Ota-ona sayfa nomi
                    'child': 'Kitob Qo\'shish'  # Hozirgi sahifa nomi
                }
                return render(request, 'applications/library/createBook/create-book.html', {'breadcrumb': breadcrumb})
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')


@login_required
def accept_book(request):
    """Band Kitoblar."""
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'Library'] and request.user.groups.filter(
                    name__in=['Administrator', 'Library']).exists():
                breadcrumb = {
                    'parent': 'Kutubxona',  # Ota-ana sayfa adı
                    'child': 'Kitoblar qabul qilish'  # Mevcut sayfa adı
                }
                return render(request, 'applications/library/acceptBook/acceptBook.html', {'breadcrumb': breadcrumb})
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')


@login_required
def seperate_book(request):
    """Kitoblarni kutubxonalarga tarqatish sahifasi."""
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'LibraryAdmin'] and request.user.groups.filter(
                    name__in=['Administrator', 'Library']).exists():
                breadcrumb = {
                    'parent': 'Kutubxona',  # Ota-ana sayfa adı
                    'child': 'Kitoblarni kutubxonalarga tarqatish'  # Mevcut sayfa adı
                }
                return render(request, 'applications/library/seperation/seperation.html', {'breadcrumb': breadcrumb})
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')


@login_required
def statistics_library(request):
    """Statistika sahifasi."""
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'Library', 'LibraryAdmin'] and request.user.groups.filter(
                    name__in=['Administrator', 'Library', 'LibraryAdmin']).exists():
                # Hozirgi yilni olish
                hozirgi_yil = datetime.now().year

                breadcrumb = {
                    'parent': 'Kutubxona',  # Ota-ana sayfa adı
                    'child': 'Statistika'  # Mevcut sayfa adı
                }
                return render(request, 'applications/library/statistics/statistics.html', {'breadcrumb': breadcrumb, 'hozirgi_yil': hozirgi_yil})
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')

@login_required
def give_book_view(request):
    """Kitob berish sahifasi."""
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'Library', 'LibraryAdmin'] and request.user.groups.filter(
                    name__in=['Administrator', 'Library', 'LibraryAdmin']).exists():
                breadcrumb = {
                    'parent': 'Kutubxona',  # Ota-ana sayfa adı
                    'child': 'Kitob berish'  # Mevcut sayfa adı
                }
                return render(request, 'applications/library/giveBook/giveBook.html', {'breadcrumb': breadcrumb})
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')



@login_required
def book_tables(request):
    """Kitoblar jadvali"""
    if request.user.is_authenticated:
        user_url = request.user.now_role.lower()
        if request.user.groups.exists():
            if request.user.now_role in ['Administrator', 'Library',
                                         'LibraryAdmin'] and request.user.groups.filter(
                    name__in=['Administrator', 'Library', 'LibraryAdmin']).exists():
                breadcrumb = {
                    'parent': 'Kutubxona',  # Ota-ana sayfa adı
                    'child': 'Kitoblar jadvali',
                    'url': 'book_tables'# Sayt urlli
                }
                return render(request, 'applications/library/bookTable/bookTable.html',
                              {'breadcrumb': breadcrumb})
            else:
                return redirect('index')
        else:
            return redirect('error')
    else:
        return redirect('login')



