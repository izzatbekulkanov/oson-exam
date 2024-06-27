from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from account.models import CustomUser
from .models import Library, Book, BookLoan, BookOrder, BookType, Author, BookCopy, BBK

class LibraryInline(admin.TabularInline):
    model = Library.small_librarians.through

class CustomUserAdmin(UserAdmin):
    inlines = [LibraryInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'number', 'university', 'created_date', 'updated_date', 'big_librarian', 'active')
    list_filter = ('university', 'active', 'created_date', 'updated_date')
    search_fields = ('name', 'address', 'number')
    readonly_fields = ('created_date', 'updated_date')
    autocomplete_fields = ('big_librarian',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "small_librarians":
            kwargs["queryset"] = CustomUser.objects.filter(groups__name="Library")
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'quantity', 'publication_year', 'status', 'added_by_full_name', 'book_type', 'view_book_card']
    list_editable = ['status']
    list_filter = ['publication_year', 'created_at', 'updated_at']
    search_fields = ['title', 'authors__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': (
                'title', 'authors', 'pages', 'quantity', 'book_type',  'image', 'file', 'publication_year', 'status', 'is_online','isbn', 'language', 'added_by', 'bookCard') # 'added_by' ustunini qo'shing
        }),
        ("Vaqt ma'lumotlari", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.added_by: # Agar 'added_by' ustuni to'ldirilmagan bo'lsa
            obj.added_by = request.user # 'added_by' ustuniga joriy foydalanuvchi beriladi
        obj.save() # Saqlash

    def added_by_full_name(self, obj):
        """Foydalanuvchi to'liq ismini qaytarish."""
        if obj.added_by:
            return obj.added_by.full_name
        return "Unknown"

    added_by_full_name.short_description = 'Added By'

    def view_book_card(self, obj):
        """Kitob kartinin ko'rish uchun tugma."""
        if obj.bookCard:
            return format_html('<a href="{}" target="_blank">View Card</a>', obj.bookCard.url)
        return "-"
    view_book_card.short_description = "Book Card"

@admin.register(BookType)
class BookTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')  # Ro'yxatda nameni ko'rsatish

@admin.register(BBK)
class BBKAdmin(admin.ModelAdmin):
    list_display = ['name', 'code','created_at', 'updated_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'title']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['original_book', 'book_id', 'barcode_display', 'inventory_number', 'created_at', 'updated_at', 'send_date', 'accept_date']
    search_fields = ['original_book__title', 'book_id']

    def barcode_display(self, obj):
        if obj.barcode_book:
            return format_html('<img src="{}" width="100" height="50" />'.format(obj.barcode_book.url))
        return "No barcode"

    barcode_display.short_description = 'Barcode Image'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email', 'author_code', 'is_active', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']  # book_count readonly bo'lishi mumkin
    list_filter = ['is_active']
    search_fields = ['name', 'author_code']

    def barcode_display(self, obj):
        """Bar code qismi uchun rasmini ko'rsatish."""
        if obj.barcode:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.barcode.url,
                width=100,
                height=50,
            ))
        return "No barcode"

    barcode_display.short_description = 'Barcode Image'

    def available_quantity_display(self, obj):
        return obj.available_quantity

    available_quantity_display.short_description = 'Available Quantity'

    def book_id_display(self, obj):
        return obj.book_id

    book_id_display.short_description = 'Book ID'

@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'id', 'user', 'loan_date', 'return_date', 'status']
    list_filter = ['status', 'loan_date', 'library']
    search_fields = ['book__title', 'user__username',  'user__email']
    readonly_fields = ['loan_date']
    fieldsets = (
        (None, {
            'fields': ('book', 'user', 'loan_date', 'status', 'library', 'quantity', 'return_date', 'status_date', 'commentary')
        }),
    )

@admin.register(BookOrder)
class BookOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'book_title', 'authors', 'order_date', 'status']
    list_filter = ['status', 'order_date']
    search_fields = ['user__email', 'book_title', 'authors']
    readonly_fields = ['order_date']

    def authors(self, obj):
        return obj.get_authors()