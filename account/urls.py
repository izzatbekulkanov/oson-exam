from django.middleware.csrf import get_token
from django.urls import path

from .employeeViews import employee_list_json, get_employee_info, create_employee_from_api
from .roleViews import group_list, create_default_groups
from .studentViews import save_student_from_api, create_student_from_api, get_student_info, student_list_json
from .views import login_view, logout, student_list, employee_list, user_list

login_patterns = [
    path('login', login_view, name='login'),
    path('logout', logout, name='logout'),
]

student_patterns = [
    path('student_list_json', student_list_json, name='student_list_json'),
    path('save_student_from_api', save_student_from_api, name='save_student_from_api'),
    path('create_student_from_api', create_student_from_api, name='create_student_from_api'),
    path('get_student_info', get_student_info, name='get_student_info'),
]
employee_patterns = [
    path('employee_list_json', employee_list_json, name='employee_list_json'),
    path('get_employee_info', get_employee_info, name='get_employee_info'),
    path('create_employee_from_api', create_employee_from_api, name='create_employee_from_api'),
]

role_permissions = [
    path('group_list_api', group_list, name='group_list'),
    path('create_default_groups', create_default_groups, name='create_default_groups'),
]



views_patterns = [
    # Hodimlar haqida ma'lumotni olish uchun URL
    path('student_list', student_list, name='student_list'),
    path('employee_list', employee_list, name='employee_list'),
    path('user_list', user_list, name='user_list'),

]

urlpatterns = views_patterns + login_patterns + role_permissions + employee_patterns + student_patterns
