# views.py
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from ...models import BookCopy, Book, BookLoan
from django.db import transaction


@require_POST
def delete_book_copies(request):
    try:
        book_id = request.POST.get('book_id')
        selected_copies = request.POST.getlist('copies')

        print(selected_copies)

        with transaction.atomic():  # Ma'lumotlar bazasi operatsiyalarining atomligini ta'minlash
            # Kitobni olish
            book = get_object_or_404(Book, id=book_id)

            # Tanlangan nusxalar bilan bog'liq biron bir BookLoan obyektlari mavjudligini tekshirish
            if not BookLoan.objects.filter(book__id__in=selected_copies).exists():
                # Barcha tanlangan BookCopy obyektlarini o'chirish
                for copy_id in selected_copies:
                    copy = get_object_or_404(BookCopy, id=copy_id)
                    copy.delete()

                # Agar barcha nusxalar o'chirilgan bo'lsa, Book obyektini ham o'chirish
                if book.copies.count() == 0:
                    book_title = book.title  # O'chirishdan oldin kitob nomini saqlash
                    book.delete()
                    response_data = {'success': True, 'message': f'Tanlangan "{book_title}" nusxalari o\'chirildi'}
                else:
                    book.quantity = book.copies.count()
                    book.save()
                    response_data = {'success': True, 'message': f'Tanlangan "{book.title}" nusxalari muvaffaqiyatli o\'chirildi'}
            else:
                # Agar tanlangan nusxalar bilan bog'liq BookLoan obyektlari mavjud bo'lsa, o'chirish mumkin emas
                response_data = {'success': False, 'message': 'Ushbu kitobga tegishli obunachilar mavjud. Kitob nusxalari o\'chirilmadi.'}

    except Book.DoesNotExist:
        response_data = {'success': False, 'message': 'Kitob topilmadi'}

    except BookCopy.DoesNotExist:
        response_data = {'success': False, 'message': 'Kitob nusxasi topilmadi'}

    except Exception as e:
        response_data = {'success': False, 'message': str(e)}

    return JsonResponse(response_data)