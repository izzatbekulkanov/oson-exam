from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as django_logout
from django.shortcuts import render, redirect
from django.utils import timezone

from log.models import LogEntry


def login_view(request):
    if request.user.is_authenticated:
        # Redirect based on user role
        if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Employee').exists():
            request.session['login_via'] = 'login_view'
            save_log(request, 'Login', f'User {request.user.get_full_name()} logged in as Admin/Employee from IP: {get_client_ip(request)}')
            return redirect('a_dashboard')
        else:
            request.session['login_via'] = 'login_view'
            save_log(request, 'Login', f'User {request.user.get_full_name()} logged in as User from IP: {get_client_ip(request)}')
            return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Correct usage of login function
            messages.success(request, 'Tizimga muvaffaqiyatli kirdingiz.')
            request.session['login_via'] = 'login_view'
            # Redirect based on user role
            if user.groups.filter(name='Admin').exists() or user.groups.filter(name='Employee').exists():
                save_log(request, 'Login', f'User {user.get_full_name()} logged in as Admin/Employee from IP: {get_client_ip(request)}')
                return redirect('a_dashboard')
            else:
                save_log(request, 'Login', f'User {user.get_full_name()} logged in as User from IP: {get_client_ip(request)}')
                return redirect('dashboard')
        else:
            messages.error(request, 'Email yoki parol xato.')
            save_log(request, 'ERROR', f'Failed login attempt for username: {username} from IP: {get_client_ip(request)}')

    return render(request, 'pages/login.html')


def logout(request):
    if request.user.is_authenticated:
        save_log(request, 'Logout', f'User {request.user.get_full_name()} logged out from IP: {get_client_ip(request)}')
    django_logout(request)
    return redirect('dashboard')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def save_log(request, level, message):
    user_full_name = request.user.get_full_name() if request.user.is_authenticated else None
    browser_info = request.META.get('HTTP_USER_AGENT', '')[:100]  # Get browser name and version
    browser_name = browser_info.split()[0] if browser_info else None
    mac_address = None  # MAC address can't be reliably obtained in web applications
    device_name = browser_name  # Use browser name as device name
    global_ip = get_client_ip(request)


    LogEntry.objects.create(
        timestamp=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        level=level,
        message=message,
        user_full_name=user_full_name,
        browser_name=browser_name,
        mac_address=mac_address,
        device_name=device_name,
        global_ip=global_ip,
    )

