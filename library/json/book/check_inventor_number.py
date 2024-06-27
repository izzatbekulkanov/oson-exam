from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST

from ...models import BookCopy, Book


@require_http_methods(["GET"])  # Faqat GET so'rovlarni qabul qilish
def check_inventory_existence(request):
    kitob_id = request.GET.get('kitob_id')
    inventory_number = request.GET.get('inventory_number')
    inventar_start = request.GET.get('inventar_start')
    inventar_end = request.GET.get('inventar_end')

    # Qo'shimcha tekshiruvlar
    if not kitob_id or not inventory_number or not inventar_start or not inventar_end:
        return JsonResponse({'error': 'All parameters must be provided'}, status=400)

    try:
        # Kitobga tegishli BookCopy obyektlarini topish
        existing_copies = BookCopy.objects.filter(
            original_book_id=kitob_id,
            inventory_number__startswith=inventory_number
        )

        # Berilgan start va end raqamlar ichida mavjud bo'lgan inventar raqamlarini tekshirish
        existing_inventory_numbers = []
        for copy in existing_copies:
            # inventory_number'ni parslash
            try:
                number_part = int(copy.inventory_number.split('/')[-1])
                if inventar_start and inventar_end:  # Agar inventar_start va inventar_end bo'sh bo'lmasa
                    if int(inventar_start) <= number_part <= int(inventar_end):
                        existing_inventory_numbers.append(copy.inventory_number)
            except (ValueError, TypeError) as e:
                continue

        if inventar_start and inventar_end:
            if int(inventar_end) < int(inventar_start):
                return JsonResponse({'error': 'Inventar end raqami inventar start raqamidan kichik bo\'lishi mumkin emas.'}, status=400)

        # Agar mavjud bo'lmagan inventar raqamlar bo'lsa 200 status bilan bo'sh javob qaytariladi
        if not existing_inventory_numbers:
            return JsonResponse({'message': 'Mavjud inventar kiritish uchun yaroqli'}, status=200)

        response_data = {
            'exists_inventories': existing_inventory_numbers
        }
        return JsonResponse(response_data, status=202)  # Status 202 OK
    except Exception as e:
        print(f"Exception occurred: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
def save_book_copies(request):
    if request.method == 'POST':
        kitob_id = request.POST.get('kitob_id')
        inventory_number = request.POST.get('inventory_number')
        inventar_start = request.POST.get('inventar_start')
        inventar_end = request.POST.get('inventar_end')

        try:
            book = Book.objects.get(id=kitob_id)
            create_book_copies(book, inventory_number, inventar_start, inventar_end)
            return JsonResponse({'success': True})
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def create_book_copies(book, inventory_number, inventar_start, inventar_end):
    """
    Ushbu funksiya kitob nusxalarini yaratadi va quantity ni yangilaydi.

    :param book: Kitob obyekti
    :param inventory_number: Inventar raqami
    :param inventar_start: Boshlang'ich inventar raqami
    :param inventar_end: Tugash inventar raqami
    """
    # Boshlang'ich raqamni olish
    start_number = int(inventar_start.split('/')[-1])

    # Tugash raqamni olish
    end_number = int(inventar_end.split('/')[-1])

    # Boshlang'ich raqamdan tugash raqamgacha iteratsiya qilish
    for i in range(start_number, end_number + 1):
        # Har bir inventar raqamni formatlash
        inventar_number = f'{inventory_number}/{i}'

        # BookCopy modelida yangi kitob nusxasini yaratish
        BookCopy.objects.create(
            original_book=book,
            status='not_accepted',  # Yangi kitob nusxasining dastlabki holati
            inventory_number=inventar_number  # Formatlangan inventar raqam
        )

    # Kitob obyekti quantity sonini yangilash
    book.quantity += (end_number - start_number + 1)
    book.save()