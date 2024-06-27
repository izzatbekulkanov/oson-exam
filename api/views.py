from rest_framework import generics, filters
from library.models import Book, Library
from .serializers import BookSerializer, LibrarySerializer
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import StandardResultsSetPagination

class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['library', 'book_type', 'bbk', 'authors']
    search_fields = ['title', 'isbn', 'authorCode']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Agar query params bo'lmasa, barcha kitoblarni qaytaradi
        filter_params = self.request.query_params
        if not any(filter_params.values()):
            return queryset
        return queryset

class LibraryListAPIView(generics.ListAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Agar query params bo'lmasa, barcha kutubxonalarni qaytaradi
        filter_params = self.request.query_params
        if not any(filter_params.values()):
            return queryset
        return queryset