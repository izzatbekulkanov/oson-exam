import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


from ...models import BookCopy, Library
from ...serializers import BookCopySerializer
from collections import defaultdict


def get_sent_books_by_bbk(request):
    user = request.user

    # Foydalanuvchi small librarian bo'lib birikkan kutubxonalar
    user_libraries = Library.objects.filter(small_librarians=user)

    # Sent statusiga ega bo'lgan kitob nusxalari va foydalanuvchining kutubxonalariga tegishli bo'lganlar
    sent_copies = BookCopy.objects.filter(status='sent', library__in=user_libraries)

    copies_by_day = defaultdict(list)
    for copy in sent_copies:
        sent_date = str(copy.send_date.date())  # Datetime obyektini matnga o'zgartiramiz
        copies_by_day[sent_date].append(copy)

    serialized_copies_by_day = {}
    for sent_date, copies in copies_by_day.items():
        serialized_copies_by_day[sent_date] = BookCopySerializer(copies, many=True).data

    return JsonResponse(serialized_copies_by_day)



def get_sent_books_by_date(request):
    date = request.GET.get('date')
    if date:
        # Berilgan sana uchun sent statusiga ega bo'lgan kitob nusxalari
        sent_copies = BookCopy.objects.filter(status='sent', send_date__date=date)
        serialized_copies = BookCopySerializer(sent_copies, many=True).data
        return JsonResponse(serialized_copies, safe=False)
    else:
        return JsonResponse({'error': 'Date parameter is missing'}, status=400)


@csrf_exempt
def accept_book_copies(request):
    if request.method == "POST":
        data = json.loads(request.body)
        copies = data.get('copies', [])

        now_date = timezone.now()

        # BookCopy obyektlarini yangilash
        BookCopy.objects.filter(inventory_number__in=copies).update(status='accepted', accept_date=now_date)

        return JsonResponse({"message": "Book copies accepted successfully"}, status=200)


def get_accept_books_by_bbk(request):
    user = request.user

    # Foydalanuvchi small librarian bo'lib birikkan kutubxonalar
    user_libraries = Library.objects.filter(small_librarians=user)

    # Sent statusiga ega bo'lgan kitob nusxalari va foydalanuvchining kutubxonalariga tegishli bo'lganlar
    sent_copies = BookCopy.objects.filter(status='accepted', library__in=user_libraries)

    copies_by_day = defaultdict(list)
    for copy in sent_copies:
        sent_date = str(copy.send_date.date())  # Datetime obyektini matnga o'zgartiramiz
        copies_by_day[sent_date].append(copy)

    serialized_copies_by_day = {}
    for sent_date, copies in copies_by_day.items():
        serialized_copies_by_day[sent_date] = BookCopySerializer(copies, many=True).data

    return JsonResponse(serialized_copies_by_day)