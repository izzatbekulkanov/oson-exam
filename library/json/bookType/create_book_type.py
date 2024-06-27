import json
from sqlite3 import IntegrityError

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from library.models import BookType, BBK, Book, BookCopy
from django.db.models import Count, Sum



@login_required
@require_POST
def create_book_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')  # Name of the book type
        image = request.FILES.get('image')  # Image file for the book type
        user = request.user

        print(name, image)

        # Check if the name is provided
        if not name:
            return JsonResponse({'error': 'Name is required.'}, status=400)

        try:
            existing_book_type = BookType.objects.get(name=name)
            return JsonResponse({'error': f'Book type "{name}" already exists.', 'id': existing_book_type.id},
                                status=400)
        except ObjectDoesNotExist:
            # Create the new book type
            book_type = BookType.objects.create(name=name, image=image, user=user)

            # Return success response
            return JsonResponse({'message': 'Book type created successfully.', 'id': book_type.id}, status=201)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


@login_required
def get_all_book_types(request):
    # Tüm BookType örneklerini alın ve ilişkili kitoblar va bbklar sayısını sayın
    book_types = BookType.objects.annotate(total_books=Sum('books__quantity')).order_by('name')

    # BookType örneklerinin detaylarını toplamak için bir liste oluşturun
    book_type_list = []
    for book_type in book_types:
        # Yaratılan va yangilangan vaqtlarni istenilen formatda kiritish
        created_at = book_type.created_at.strftime("%Y-%m-%d | %H:%M")
        updated_at = book_type.updated_at.strftime("%Y-%m-%d | %H:%M")

        # Kitoblar soni
        total_books = Book.objects.filter(book_type=book_type).count()

        # Kitob nusxalari soni
        book_copies = BookCopy.objects.filter(original_book__book_type=book_type).count()

        book_type_data = {
            'id': book_type.id,
            'name': book_type.name,
            'image_url': book_type.image_url(),
            'created_at': created_at,
            'updated_at': updated_at,
            'is_active': book_type.is_active,
            'user': book_type.user.username if book_type.user else None,
            'total_books': total_books,
            'total_book_copies': book_copies,  # Kitob nusxalari soni
        }
        book_type_list.append(book_type_data)

    # JSON ma'lumotlarini tayyorlash va qaytarish
    data = {'book_types': book_type_list}
    return JsonResponse(data)


@csrf_exempt
def create_bbk(request):
    data = json.loads(request.body)
    bbk_name = data.get('name', '')
    bbk_title = data.get('title')
    bbk_is_active = data.get('is_active')

    try:
        # BBK nomini tekshirish
        existing_bbk = BBK.objects.filter(name=bbk_name).first()
        if not existing_bbk:
            # Agar BBK mavjud bo'lmasa, yangi BBK obyektini yaratish
            new_bbk = BBK.objects.create(
                name=bbk_title,
                code=bbk_name,

                is_active=bbk_is_active
            )
            # BBK muvaffaqiyatli saqlansa muvaffaqiyatli saqlandi xabarini qaytarish
            response_data = {
                'message': 'BBK muvaffaqiyatli saqlandi'
            }
        else:
            # Agar BBK mavjud bo'lsa, "Bunday nomdagi BBK avvaldan mavjud" xabarni qaytarish
            response_data = {
                'message': 'Bunday nomdagi BBK avvaldan mavjud'
            }
    except IntegrityError:
        # IntegrityError yuzaga kelganda ham "Bunday nomdagi BBK avvaldan mavjud" xabarni qaytarish
        response_data = {
            'message': 'Bunday nomdagi BBK avvaldan mavjud'
        }

    return JsonResponse(response_data)


def get_all_bbks(request):
    bbks = BBK.objects.all().order_by('code')  # 'code' maydoni bo'yicha tartiblash
    bbk_list_with_president = []
    bbk_list_without_president = []

    for bbk in bbks:
        # BBK obyektining kitoblari sonini hisoblash
        books = Book.objects.filter(bbk=bbk)
        book_count = books.count()

        # BBK obyektining kitob nusxalari sonini hisoblash
        book_copy_count = BookCopy.objects.filter(original_book__in=books).count()

        bbk_data = {
            'id': bbk.id,
            'name': bbk.name,
            'title': bbk.code,
            'created_at': bbk.created_at.strftime("%Y-%m-%d | %H:%M"),
            'updated_at': bbk.updated_at.strftime("%Y-%m-%d | %H:%M"),
            'is_active': bbk.is_active,
            'book_count': book_count,  # BBK obyektining kitoblari soni
            'book_copy_count': book_copy_count  # BBK obyektining kitob nusxalari soni
        }

        if 'prezident' in bbk.name.lower():
            bbk_list_with_president.append(bbk_data)
        else:
            bbk_list_without_president.append(bbk_data)

    # Ro'yxatlarni birlashtirish: 'prezident' so'zi mavjud bo'lganlarni boshiga qo'yamiz
    bbk_list = bbk_list_with_president + bbk_list_without_president

    return JsonResponse({'bbks': bbk_list})

@csrf_exempt
def update_bbk(request):
    if request.method == 'POST':


        data = json.loads(request.body)
        print(data)
        bbk_name = data.get('name', '')
        bbk_code = data.get('title')
        bbk_id = data.get('id')

        try:
            bbk = BBK.objects.get(id=bbk_id)
            bbk.name = bbk_name
            bbk.code = bbk_code
            bbk.save()
            message = 'BBK updated successfully.'
            status_code = 200
        except ObjectDoesNotExist:
            bbk = BBK(name=bbk_name, code=bbk_code)
            bbk.save()
            message = 'BBK created successfully.'
            status_code = 201

        return JsonResponse({'message': message}, status=status_code)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)
