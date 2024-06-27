from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import os
from library.models import Book, Author, BookCopy, BookType, BBK

@csrf_exempt
def save_book(request):
    if request.method == 'POST':
        required_fields = ['title', 'authors', 'authorCode', 'page', 'language', 'publisher_city', 'publication_year', 'publisher', 'isbn', 'adad', 'inventar_seriya', 'quantity', 'annotation', 'category_book', 'bbk_book']
        for field in required_fields:
            if not request.POST.get(field):
                return JsonResponse({'success': False, 'message': f'{field} maydoni talab qilinadi'}, status=400)

        # Formdan ma'lumotlarni olish
        title = request.POST.get('title')
        authors = request.POST.get('authors')
        authorCode = request.POST.get('authorCode')
        pages = request.POST.get('page')
        language = request.POST.get('language')
        publisher_city = request.POST.get('publisher_city')
        publication_year = request.POST.get('publication_year')
        publisher = request.POST.get('publisher')
        isbn = request.POST.get('isbn')
        adad = request.POST.get('adad')
        inventar_start = request.POST.get('inventar_seriya')
        quantity = request.POST.get('quantity')
        annotation = request.POST.get('annotation')
        user = request.user

        # ISBN mavjudligini tekshirish
        if Book.objects.filter(isbn=isbn).exists():
            return JsonResponse({'success': False, 'message': 'Ushbu ISBN ga ega kitob bazada mavjud'}, status=400)

        # Inventory raqami mavjudligini tekshirish
        parts = inventar_start.split()
        if len(parts) == 2:
            start_char, start_number = parts
            start_number = (start_number)
            for i in range(1, int(quantity) + 1):
                inventar_number = f'{start_char} {start_number}/{i}'
                if BookCopy.objects.filter(inventory_number=inventar_number).exists():
                    return JsonResponse({'success': False, 'message': f'Inventar raqami {inventar_number} bazada mavjud'}, status=400)
        else:
            start_number = (parts[0])
            for i in range(1, int(quantity) + 1):
                inventar_number = f'{start_number}/{i}'
                if BookCopy.objects.filter(inventory_number=inventar_number).exists():
                    return JsonResponse({'success': False, 'message': f'Inventar raqami {inventar_number} bazada mavjud'}, status=400)

        # Category book va BBK bookni olish
        category_book_id = request.POST.get('category_book')
        bbk_book_id = request.POST.get('bbk_book')

        # Kategoriyani olish
        try:
            book_type = get_object_or_404(BookType, id=category_book_id)
        except BookType.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Kategoriyani topib bo\'lmadi'}, status=400)

        # BBK ni olish
        try:
            bbk = get_object_or_404(BBK, id=bbk_book_id)
        except BBK.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'BBK topib bo\'lmadi'}, status=400)

        # Fayl yuklash logikasi (rasm va PDF)
        image = request.FILES.get('image')
        file = request.FILES.get('file')

        # Kitob yaratishdan oldin kerakli maydonlarni tekshirish
        if not (title and authors and isbn and inventar_start and quantity):
            return JsonResponse({'success': False, 'message': 'Kerakli maydonlar yetarli emas'}, status=400)

        # Kitob yaratish
        book = Book(
            title=title,
            book_type=book_type,
            authorCode=authorCode,
            bbk=bbk,
            quantity=quantity,
            adad=adad,
            pages=pages,
            language=language,
            publication_year=publication_year,
            publisher=publisher,
            isbn=isbn,
            added_by=user,
            published_city=publisher_city,
            annotation=annotation,
            status='undistributed'
        )

        # Kitobni saqlash
        book.save()

        # Mualliflar ro'yxati (qatorlar bo'yicha ajratib olish)
        authors_list = [author.strip() for author in authors.split(',')]
        for author_name in authors_list:
            author, created = Author.objects.get_or_create(name=author_name)
            book.authors.add(author)

        # Rasmni saqlash (agar mavjud bo'lsa)
        if image:
            book.image = image

        # PDF faylni saqlash (agar mavjud bo'lsa)
        if file:
            book.file = file

        # Kitob kartinig tayyorlash va saqlash
        create_book_card(book)

        # Kitob nusxalarini yaratish
        parts = inventar_start.split()
        if len(parts) == 2:
            start_char, start_number = parts
            start_number = (start_number)  # Boshlang'ich inventar raqamini olish
            for i in range(1, int(quantity) + 1):
                inventar_number = f'{start_char} {start_number}/{i}'
                BookCopy.objects.create(
                    original_book=book,
                    status='not_accepted',
                    inventory_number=f'{inventar_number}'
                )
        else:
            start_number = (parts[0])  # Faqat raqam
            for i in range(1, int(quantity) + 1):
                inventar_number = f'{start_number}/{i}'
                BookCopy.objects.create(
                    original_book=book,
                    status='not_accepted',
                    inventory_number=f'{inventar_number}'
                )

        # Saqlash jarayonini tugatish
        book.save()

        return JsonResponse({'success': True, 'message': 'Kitob saqlandi'}, status=201)
    else:
        return JsonResponse({'success': False, 'message': 'Noto\'g\'ri so\'rov turi'}, status=400)


def create_book_card(book):
    # Kitob ma'lumotlarini to'plash
    context = {
        'title': book.title,
        'authors': ', '.join([author.name for author in book.authors.all()]),
        'authorCode': book.authorCode,
        'publisher_city': book.published_city,
        'publisher': book.publisher,
        'publication_year': book.publication_year,
        'isbn': book.isbn,
        'book_type': book.book_type.name if book.book_type else '',
        'bbk_code': book.bbk.name if book.bbk else '',
    }

    # Yangi karta tayyorlash (oq fon)
    card_width = 1250
    card_height = 750
    new_card = Image.new('RGB', (card_width, card_height), color='white')
    draw = ImageDraw.Draw(new_card)

    # Font yo'lini aniqlash
    font_path = os.path.join(settings.STATIC_ROOT, 'assets/fonts/arial.ttf')
    font = ImageFont.truetype(font_path, 20)

    # Karta ma'lumotlarini joylash
    y_text = 20
    for key, value in context.items():
        draw.text((20, y_text), f"{key.replace('_', ' ').title()}: {value}", font=font, fill="black")
        y_text += 40

    # Karta saqlash
    card_name = os.path.join(settings.MEDIA_ROOT, f"book_cards/{book.id}_card.png")
    new_card.save(card_name)

    # Karta manzilini kitob obyektiga saqlash
    book.bookCard = f"book_cards/{book.id}_card.png"
    book.save()

    return JsonResponse({'success': True, 'message': 'Kitob kartasi yaratildi'}, status=200)