import os
import random
import string
from datetime import timedelta
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from account.models import CustomUser
from core import settings
from university.models import University
from django.utils import timezone

from django.core.files import File
import os

User = get_user_model()


def generate_book_id():
    """Kitob identifikatorini avtomatik tarzda yaratish."""
    return '451' + ''.join(random.choices(string.digits, k=6))


def generate_barcode_book(book_id):
    """Kitob uchun QR kodni avtomatik tarzda yaratish."""
    CODE128 = barcode.get_barcode_class('code128')
    code128 = CODE128(book_id, writer=ImageWriter())
    buffer = BytesIO()
    code128.write(buffer)
    return buffer.getvalue()


def validate_file_extension(value):
    """Faylning formatini tekshirish uchun validator."""
    allowed_extensions = ['.pdf', '.doc', '.docx']
    file_extension = value.name.split('.')[-1]
    if file_extension not in allowed_extensions:
        raise ValidationError(_("Faqat PDF va Word fayllarini yuklab olish mumkin."))


class Library(models.Model):
    name = models.CharField(max_length=255, help_text="Kutubhona nomi")
    address = models.CharField(max_length=255, help_text="Manzili")
    number = models.CharField(max_length=255, help_text="Kutubhona raqami")
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='libraries', null=True,
                                   blank=True, help_text="University kutubhona")
    created_date = models.DateField(auto_now_add=True, help_text="Model yaratilgan sana")
    updated_date = models.DateField(auto_now=True, help_text="Model yangilangan sana")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_libraries',
                             help_text="Kutubhona yaratgan foydalanuvchi")
    big_librarian = models.ForeignKey(CustomUser, related_name='big_librarian_libraries', on_delete=models.CASCADE,
                                      null=True, blank=True)
    small_librarians = models.ManyToManyField(CustomUser, related_name='small_librarian_libraries', blank=True)
    active = models.BooleanField(default=False, help_text="Kutubhona faol yoki emasligini ko'rsatadi")

    def __str__(self):
        return self.name


class Author(models.Model):
    """Muallif modeli."""
    name = models.CharField(max_length=255, help_text="Muallifning ismi")
    phone_number = models.CharField(max_length=300, blank=True, null=True, help_text="Muallifning telefon raqami")
    image = models.ImageField(upload_to='author_image/', blank=True, null=True,
                              help_text="Kitob muallifining rasmi (mavjud bo'lsa)")
    email = models.EmailField(max_length=300, blank=True, null=True, help_text="Muallifning email")
    author_code = models.CharField(max_length=50, unique=True, help_text="Muallif belgisi", null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text="Muallifning holati")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, help_text="Yangilangan vaqt")

    def __str__(self):
        return self.name

def get_default_book_type_cover():
    return 'default/book-type-cover.jpg'
class BookType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='book_type_covers/' ,blank=True, null=True, help_text="Kitob turi rasmi (mavjud bo'lsa)", default=get_default_book_type_cover)
    created_at = models.DateTimeField(default=timezone.now, help_text="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, help_text="Yangilangan vaqt")
    is_active = models.BooleanField(default=True, help_text="Aktiv yoki noqulayligi")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='book_types', null=True, blank=True)

    def image_url(self):
        if self.image:
            return default_storage.url(self.image.name)
        return None

    def __str__(self):
        return self.name


class BBK(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

def get_default_book_cover():
    return 'default/book-cover.png'
class Book(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'Ingliz'),
        ('tr', 'Turk'),
        ('fr', 'Fransuz'),
        ('uz', "O'zbek (lotin)"),
        ('oz', "O'zbek (kril)"),
        ('ru', 'Rus'),
        ('de', 'Nemis'),
        ('zh', 'Xitoy'),
        ('es', 'Ispan'),
        ('ko', 'Koreys'),
        ('kk', 'Qozoq'),
        ('ky', 'Qirg\'iz'),
        ('tg', 'Tojik'),
        ('qr', 'Qoraqalpoq'),
    ]
    """Kitob modeli."""
    title = models.CharField(max_length=255, help_text="Kitob sarlavhasi")
    authors = models.ManyToManyField(Author, related_name='books', help_text="Kitob mualliflari")
    authorCode = models.CharField(max_length=50, blank=True, null=True, help_text="Kitobning Mualliflik kodi")
    quantity = models.IntegerField(default=0, help_text="Kitoblar soni")
    adad = models.BigIntegerField(default=0, help_text="Kitobning adadi")  # Adad maydoni qo'shildi
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True, help_text="Kitob rasmi (mavjud bo'lsa)", default=get_default_book_cover)
    bookCard = models.ImageField(upload_to='book_cards/', blank=True, null=True, help_text="Kitob kartasi")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, related_name='books', null=True, blank=True, help_text="Kitob kutubxonasi")
    status = models.CharField(max_length=20, choices=[('distributed', 'Yakunlangan'), ('undistributed', 'Yakunlanmagan')], default='rejected', help_text="Kitob holati")
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='added_books', help_text="Kitobni qo'shgan foydalanuvchi")
    isbn = models.CharField(max_length=50, blank=True, null=True, help_text="Kitobning ISBN raqami")
    file = models.FileField(upload_to='book_files/', null=True, blank=True, validators=[validate_file_extension], help_text="Kitob fayli (faqat Word va PDF)")
    book_type = models.ForeignKey(BookType, on_delete=models.CASCADE, related_name='books', blank=True, null=True, help_text="Kitob turining nomi")
    bbk = models.ForeignKey(BBK, on_delete=models.CASCADE, related_name='books_bbk', blank=True, null=True, help_text="Kitob turining nomi")
    is_online = models.BooleanField(default=False, help_text="Onlayn yoki oflayn")
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, help_text="Kitob tili")
    publication_year = models.IntegerField(help_text="Kitob nash qilingan yili")
    publisher = models.CharField(max_length=255, help_text="Kitob nashriyoti nomi")
    published_city = models.CharField(max_length=255, help_text="Kitob nash qilingan shahri")
    annotation = models.TextField(help_text="Kitob annotatsiyasi")
    pages = models.IntegerField(help_text="Kitob sahifalar soni")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Kitob yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, help_text="Kitob oxirgi yangilanish vaqti")

    def __str__(self):
        return self.title


class BookCopy(models.Model):
    original_book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='copies', null=True, blank=True, help_text="Original book")
    book_id = models.CharField(max_length=9, unique=True, default=generate_book_id, help_text="Book identifier")
    barcode_book = models.ImageField(upload_to='barcode_books/', blank=True, null=True, help_text="Book QR code (if available)")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, related_name='bookCopies', null=True, blank=True, help_text="Kitob kutubxonasi")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation time of the book")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update time of the book")
    send_date = models.DateTimeField(help_text="Last send time of the book", null=True, blank=True)
    accept_date = models.DateTimeField(help_text="Last accept time of the book", null=True, blank=True)
    inventory_number = models.CharField(max_length=50, unique=True, help_text="Inventory number")
    status = models.CharField(max_length=20, choices=[('accepted', 'Qabul qilindi'), ('sent', 'Yuborildi'), ('not_accepted', 'Qabul qilinmagan')],default='rejected', help_text="Kitob holati")
    haveStatus = models.CharField(max_length=20, choices=[('yes', 'Mavjud'), ('no', 'Mavjud emas')],default='yes', help_text="Kitob berilganlik holati")
    accepted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='accepted_books',help_text="Kitobni qabul qilgan foydalanuvchi", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.barcode_book:
            barcode_content = generate_barcode_book(self.book_id)
            barcode_filename = f"{self.book_id}.png"

            # Fayl nomini to'g'rilash
            barcode_file_name = os.path.join(self.inventory_number, barcode_filename)
            barcode_file_path = os.path.join(settings.MEDIA_ROOT, 'barcode_books', barcode_file_name)

            # Faylning mavjudligini tekshirish va faylni yaratish
            if not os.path.exists(os.path.dirname(barcode_file_path)):
                os.makedirs(os.path.dirname(barcode_file_path))

            # Faylni yaratish va QR-kod ma'lumotlarini yozish
            with open(barcode_file_path, 'wb') as barcode_file:
                barcode_file.write(barcode_content)

            # Fayldan File obyektini yaratish
            with open(barcode_file_path, 'rb') as barcode_file:
                barcode_file_object = File(barcode_file)

                # barcode_book atributiga File obyektini qo'shish
                self.barcode_book.save(barcode_file_name, barcode_file_object, save=False)

            # Faylni o'chirish
            os.remove(barcode_file_path)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.original_book.title} - Copy"


class BookLoan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'kutilmoqda'),
        ('returned', 'qaytarilgan'),
        ('not_returned', 'qaytarilmadi'),
    ]
    STATUS_DATA_CHOICES = [
        ('7_days', '7 kun'),
        ('10_days', '10 kun'),
        ('15_days', '15 kun'),
        ('1_month', '1 oy'),
        ('2_months', '2 oy'),
        ('3_months', '3 oy'),
        ('4_months', '4 oy'),
        ('5_months', '5 oy'),
        ('6_months', '6 oy'),
        ('1_year', '1 yil'),
        ('2_years', '2 yil'),
    ]

    """Kitob berish modeli."""
    book = models.ForeignKey('BookCopy', on_delete=models.CASCADE, help_text="Kitob")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="Foydalanuvchi")
    loan_date = models.DateTimeField(default=timezone.now, help_text="Kitob olingan vaqti")
    return_date = models.DateTimeField(blank=True, null=True, help_text="Kitobni qaytarilishi kerak bo'lgan vaqti")

    quantity = models.IntegerField(help_text="Kitob", blank=True, null=True, verbose_name="Olingan kitob soni")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',
                              help_text="Kitob bandlik holati")
    status_date = models.CharField(max_length=20, choices=STATUS_DATA_CHOICES, help_text="Kitob holati")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, related_name='book_loans', null=True, blank=True,
                                help_text="Kitob beriladigan kutubxona")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Kitob berilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, help_text="Kitob oxirgi berilgan vaqti")
    commentary = models.TextField(help_text="Kitob berilgan haqida batafsil ma'lumot", null=True, blank=True)

    def __str__(self):
        return f"{self.book} - {self.user}"

    def save(self, *args, **kwargs):
        # Agar return_date saqlanmagan bo'lsa, status_date ni avtomatik ravishda belgilash
        for status_choice, status_text in self.STATUS_DATA_CHOICES:
            if status_choice == self.status_date:
                days = int(status_choice.split('_')[0])
                self.return_date = self.loan_date + timedelta(days=days)
                break
        super().save(*args, **kwargs)

    def check_return_status(self):
        """Kitobni qaytarilganligini tekshirish va qaytarilish muddatini hisoblash."""
        if self.status != 'returned':
            loan_duration = timezone.now() - self.loan_date
            if self.status_date in ['7_days', '10_days', '15_days', '1_month', '2_months', '3_months', '4_months',
                                    '5_months', '6_months', '1_year', '2_years']:
                duration_map = {
                    '7_days': 7,
                    '10_days': 10,
                    '15_days': 15,
                    '1_month': 30,
                    '2_months': 60,
                    '3_months': 90,
                    '4_months': 120,
                    '5_months': 150,
                    '6_months': 180,
                    '1_year': 365,
                    '2_years': 730,
                }
                max_loan_duration = timedelta(days=duration_map[self.status_date])
                if loan_duration > max_loan_duration:
                    self.status = 'not_returned'
                    self.save()
                    return True
        return False


class BookOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlangan'),
        ('canceled', 'To\'xtatilgan'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(auto_now_add=True, help_text="Kitobga buyurtma vaqti")
    updated_date = models.DateTimeField(auto_now=True, help_text="Kitobga buyurtma oxirgi vaqti")

    def __str__(self):
        return f"{self.book_title} - {self.user}"
