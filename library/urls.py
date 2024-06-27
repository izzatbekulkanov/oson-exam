from django.urls import path

from library.json.acceptBook.acceptBook import get_sent_books_by_bbk, get_sent_books_by_date, accept_book_copies, \
    get_accept_books_by_bbk
from library.json.add_library import create_library_json, get_librarians_per_university, get_library_admins, \
    assign_big_librarian, get_small_librarians, assign_small_librarian
from library.json.book.authors import authors_list, get_book_authors
from library.json.book.check_inventor_number import check_inventory_existence, save_book_copies
from library.json.book.create_book import save_book
from library.json.book.book_list import get_recently_added_books, get_book_types
from library.json.book.get_book_details import get_book_details
from library.json.bookType.create_book_type import create_book_type, get_all_book_types, create_bbk, get_all_bbks
from library.json.librarien.librarian import LibraryAndAdminUsersView
from library.json.library_list import libraries_list
from library.json.seperate.seperate import assign_book_copies_to_library, get_books_by_book_type_and_bbk, \
    get_user_libraries, select_book_copy, get_not_accepted_book_copies
from library.json.statistics.statistics import library_stats_by_language
from library.views import book_list, add_book_view, book_category, library_admin_views, \
    seperate_book, library_views, accept_book, book_bbk_list, all_book_list, statistics_library, give_book_view

from library.json.bookType.create_book_type import update_bbk

from library.views import book_tables

from library.json.book.filter_book import filter_books

from library.json.book.update_book import update_book_details

from library.json.book.delete_book_copy import delete_book_copies

json_patterns = [
    path("create_library_json", create_library_json, name="create_library_json"),
    path("libraries_list", libraries_list, name="libraries_list"),
    path("get_librarians_per_university", get_librarians_per_university, name="get_librarians_per_university"),
    path("get_library_admins", get_library_admins, name="get_library_admins"),
    path("get_small_librarians", get_small_librarians, name="get_small_librarians"),
    path('assign_big_librarian', assign_big_librarian, name='assign_big_librarian'),  # Manzilni qo'shing
    path('assign_small_librarian/', assign_small_librarian, name='assign_small_librarian'),
    path('get_all_book_types', get_all_book_types, name='get_all_book_types'),
    path('create_bbk', create_bbk, name='create_bbk'),
    path('get_all_bbks', get_all_bbks, name='get_all_bbks'),
    path('update_bbk', update_bbk, name='update_bbk'),
    path('assign_book_copies_to_library', assign_book_copies_to_library, name='assign_book_copies_to_library'),
    
    path('save_book', save_book, name='save_book'),

    path('get_recently_added_books', get_recently_added_books, name='get_recently_added_books'),
    path('get_book_types', get_book_types, name='get_book_types'),


    path('library-admin-users', LibraryAndAdminUsersView.as_view(), name='library-admin-users'),
    path('get_books_by_book_type_and_bbk', get_books_by_book_type_and_bbk, name='get_books_by_book_type_and_bbk'),
    path('select_book_copy', select_book_copy, name='select_book_copy'),
    path('get_user_libraries', get_user_libraries, name='get_user_libraries'),


    path('get_sent_books_by_bbk', get_sent_books_by_bbk, name='get_sent_books_by_bbk'),
    path('get_accept_books_by_bbk', get_accept_books_by_bbk, name='get_accept_books_by_bbk'),
    path('get_sent_books_by_date', get_sent_books_by_date, name='get_sent_books_by_date'),
    path('accept_book_copies', accept_book_copies, name='accept_book_copies'),


    path('get_not_accepted_book_copies', get_not_accepted_book_copies, name='get_not_accepted_book_copies'),


    path('library_stats_by_language', library_stats_by_language, name='library_stats_by_language'),

    path('filter_books', filter_books, name='filter_books'),

    path('update_book_details/', update_book_details, name='update_book_details'),

    path('delete_book_copies', delete_book_copies, name='delete_book_copies'),


    path('check_inventory_existence', check_inventory_existence, name='check_inventory_existence'),
    path('save_book_copies', save_book_copies, name='save_book_copies'),


    path('authors_list', authors_list, name='authors_list'),
    path('get_book_authors', get_book_authors, name='get_book_authors'),




    

]

views_patterns = [
    path('library_views', library_views, name='library_views'),
    path('book_list', book_list, name='book_list'),
    path('book-bbk-list/', book_bbk_list, name='book_bbk_list'),
    path('all_book_list', all_book_list, name='all_book_list'),
    path('get_book_details', get_book_details, name='get_book_details'),


    path('statistics_library', statistics_library, name='statistics_library'),

    path('give_book_view', give_book_view, name='give_book_view'),

    path('add_book_view', add_book_view, name='add_book_view'),
    path('book_category', book_category, name='book_category'),
    path('create_book_type', create_book_type, name='create_book_type'),
    path('library_admin_views', library_admin_views, name='library_admin_views'),
    path('seperation_view', seperate_book, name='seperate_book'),
    path('accept_book', accept_book, name='accept_book'),
    path('book_tables', book_tables, name='book_tables'),
]

urlpatterns = json_patterns + views_patterns
