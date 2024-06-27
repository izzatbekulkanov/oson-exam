from rest_framework import serializers
from account.models import (
    StudentStatus, Gender, Country, Province, District, Citizenship,
    EducationForm, EducationType, EmploymentStaff, EmploymentForm, PaymentForm,
    StudentType, SocialCategory, Accommodation, Department, Curriculum,
    Specialty, GroupUniver, Level, Semester, EducationYear, EmployeeStatus,
    AcademicRank, AcademicDegree, StaffPosition, EmployeeType, Roles
)
from .models import Book, CustomUser, University, Library, BookCopy, BookType, BBK


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['name', 'address', 'number', 'university', 'created_date', 'updated_date']


class CustomUserSerializer(serializers.ModelSerializer):
    university = serializers.StringRelatedField()
    gender = serializers.StringRelatedField()
    country = serializers.StringRelatedField()
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    citizenship = serializers.StringRelatedField()
    studentStatus = serializers.StringRelatedField()
    educationForm = serializers.StringRelatedField()
    educationType = serializers.StringRelatedField()
    employmentStaff = serializers.StringRelatedField()
    employmentForm = serializers.StringRelatedField()
    paymentForm = serializers.StringRelatedField()
    studentType = serializers.StringRelatedField()
    socialCategory = serializers.StringRelatedField()
    accommodation = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    curriculum = serializers.StringRelatedField()
    specialty = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    level = serializers.StringRelatedField()
    semester = serializers.StringRelatedField()
    educationYear = serializers.StringRelatedField()
    employeeStatus = serializers.StringRelatedField()
    academikRank = serializers.StringRelatedField()
    academicDegree = serializers.StringRelatedField()
    staffPosition = serializers.StringRelatedField()
    employeeType = serializers.StringRelatedField()
    groups = serializers.StringRelatedField(many=True)
    hemis_role = serializers.StringRelatedField(many=True)

    # New fields for library association
    big_librarian_libraries = LibrarySerializer(many=True, read_only=True)
    small_librarian_libraries = LibrarySerializer(many=True, read_only=True)
    created_libraries = LibrarySerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'



class BookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookType
        fields = ['id', 'name']

class BBKSerializer(serializers.ModelSerializer):
    class Meta:
        model = BBK
        fields = ['id', 'name']
class BookSerializer(serializers.ModelSerializer):
    bookType = BookTypeSerializer(source='book_type', read_only=True)
    BBK = BBKSerializer(source='bbk', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'bookType', 'BBK', 'language', 'isbn', ]

class BookCopySerializer(serializers.ModelSerializer):
    original_book = BookSerializer()
    created_at = serializers.DateTimeField(format='%Y-%m-%d | %H:%M')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d | %H:%M')

    class Meta:
        model = BookCopy
        fields = ['original_book', 'created_at', 'updated_at', 'inventory_number']