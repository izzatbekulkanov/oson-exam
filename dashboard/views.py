from django.shortcuts import render
from django.contrib.auth.decorators import login_required




@login_required
def index(request):
    login_via = request.session.pop('login_via', None)
    set_role = request.session.pop('set_role', None)
    if login_via:
        message = f"Siz tizimga muvaffaqiyatli kirdingiz."
        type = 'info'  # Bu yerda messagetype ni aniqlang
    elif set_role:
        message = f"Siz {set_role} roliga muvaffaqiyatli o'tdingiz"
        type = 'success'
    else:
        message = None
        type = None

    return render(request, 'pages/dashboard/index.html', {'message': message, 'type': type})



