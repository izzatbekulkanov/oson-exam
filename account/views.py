from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import redirect


def login_view(request):
    if request.user.is_authenticated:
        request.session['login_via'] = 'login_view'
        return redirect('employee_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Tizimga muvaffaqiyatli kirdingiz.')
            request.session['login_via'] = 'login_view'
            return redirect('employee_dashboard')
        else:
            messages.error(request, 'Email yoki parol xato.')

    return render(request, 'pages/login.html')

