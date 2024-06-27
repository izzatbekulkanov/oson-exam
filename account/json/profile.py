import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from library.models import BookLoan


@login_required
def get_user_all_groups(request):
    if request.method == 'GET':
        # Foydalanuvchi obyektidan guruhlarni olish
        user_groups = request.user.groups.all()
        group_names = [group.name for group in user_groups]

        return JsonResponse({'success': True, 'user_groups': group_names})
    else:
        return JsonResponse({'error': 'GET so\'rov qabul qilinmaydi'}, status=400)


@login_required
def get_user_roles(request):
    if request.method == 'GET':
        # Foydalanuvchi obyektidan tegishli rollarni olish
        user_roles = request.user.hemis_role.all()

        # Rollarni nomlarini ro'yxatga joylash
        role_names = [role.name for role in user_roles]

        return JsonResponse({'success': True, 'user_roles': role_names})
    else:
        return JsonResponse({'error': 'GET so\'rov qabul qilinmaydi'}, status=400)


def format_datetime(datetime_obj):
    return datetime_obj.strftime('%Y-%m-%d %H:%M')


@login_required
def get_employee_user_information(request):
    if request.method == 'GET':
        user_info = {
            'university': request.user.university.name if request.user.university else None,
            'department': request.user.department.name if request.user.department else None,
            'curriculum': request.user.curriculum.name if request.user.curriculum else None,
            'specialty': request.user.specialty.name if request.user.specialty else None,
            'created_at': format_datetime(request.user.created_at),
            'updated_at': format_datetime(request.user.updated_at),
            'employeeStatus': request.user.employeeStatus.name if request.user.employeeStatus else None,
            'contractDate': request.user.contractDate,
            'staffPosition': request.user.staffPosition.name if request.user.staffPosition else None,
            'user_type': request.user.get_user_type_display(),
            'employeeType': request.user.employeeType.name if request.user.employeeType else None,
            'is_followers_book': request.user.is_followers_book,
            'last_login': format_datetime(request.user.last_login),
        }

        return JsonResponse({'success': True, 'user_info': user_info})
    else:
        return JsonResponse({'error': 'GET so\'rov qabul qilinmaydi'}, status=400)


@login_required
def get_user_book_loans(request):
    if request.method == 'GET':
        # Foydalanuvchi uchun barcha kitoblar
        user_book_loans = BookLoan.objects.filter(user=request.user)

        # Kutilmoqda, qaytarilgan va qaytarilmagan kitoblarni ajratib olish
        pending_loans = []
        returned_loans = []
        not_returned_loans = []

        for loan in user_book_loans:
            if loan.status == 'pending':
                pending_loans.append({
                    'book': loan.book.title,
                    'library': loan.library.name if loan.library else None,
                    'loan_date': loan.loan_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'return_date': loan.return_date.strftime('%Y-%m-%d %H:%M:%S') if loan.return_date else None,
                    'status': loan.status,
                    'commentary': loan.commentary,
                })
            elif loan.status == 'returned':
                returned_loans.append({
                    'book': loan.book.title,
                    'library': loan.library.name if loan.library else None,
                    'loan_date': loan.loan_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'return_date': loan.return_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': loan.status,
                    'commentary': loan.commentary,
                })
            elif loan.status == 'not_returned':
                not_returned_loans.append({
                    'book': loan.book.title,
                    'library': loan.library.name if loan.library else None,
                    'loan_date': loan.loan_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'return_date': loan.return_date.strftime('%Y-%m-%d %H:%M:%S') if loan.return_date else None,
                    'status': loan.status,
                    'commentary': loan.commentary,
                })

        # Ro'yxatni JSON ko'rinishida qaytarish
        return JsonResponse({
            'success': True,
            'pending_loans': pending_loans,
            'returned_loans': returned_loans,
            'not_returned_loans': not_returned_loans,
        })
    else:
        # Get so'rovi qabul qilinmadi
        return JsonResponse({'error': 'GET so\'rov qabul qilinmaydi'}, status=400)





