from rest_framework import serializers
from library.models import Book, Library, BookType, BBK, Author, BookCopy

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'
        ref_name = 'LibrarySerializerRef'

class BookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookType
        fields = '__all__'
        ref_name = 'BookTypeSerializerRef'

class BBKSerializer(serializers.ModelSerializer):
    class Meta:
        model = BBK
        fields = '__all__'
        ref_name = 'BBKSerializerRef'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        ref_name = 'AuthorSerializerRef'

class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = '__all__'
        ref_name = 'BookCopySerializerRef'

class BookSerializer(serializers.ModelSerializer):
    library = LibrarySerializer()
    book_type = BookTypeSerializer()
    bbk = BBKSerializer()
    authors = AuthorSerializer(many=True)
    book_copies = BookCopySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        ref_name = 'BookSerializerRef'