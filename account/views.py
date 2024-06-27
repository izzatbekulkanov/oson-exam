from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect



def login_view(request):
    user = request.user
    if user.is_authenticated:
        request.session['login_via'] = 'login_view'
        return redirect('index')
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('login[password]')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            request.session['login_via'] = 'login_view'
            return redirect('index')  # Change 'index' to your desired redirect path
        else:
            print("muvaffaqiyatsiz")
            messages.error(request, 'Email yoki parol xato.')
    return render(request, 'pages/authentication/login/login.html')  # Change 'your_app' to your app name

@login_required
def employee_view(request):
    return render(request, 'applications/account/employee/employee.html')

@login_required
def student_view(request):
    return render(request, 'applications/account/student/student.html')

def permission_view(request):
    return render(request, 'pages/permissions.html')


def create_student(request):
    return render(request, 'app/university/pages/create_student.html')

def student_list(request):
    return render(request, 'app/university/pages/student_list.html')

def logout_view(request):
    logout(request)
    # Foydalanuvchi logout qilinsa, u login sahifasiga qaytariladi
    return redirect('login')  # 'login' ning sizning login sahifangizga mos kelishi kerak

def create_employee_view(request):
    return render(request, 'pages/employee/../templates2/app/users/create-employee.html')

def hemis_view(request):
    return render(request, 'pages/hemis-api.html')

def profile_view(request):
    return render(request, 'app/users/profile.html')
