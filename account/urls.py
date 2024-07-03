from django.middleware.csrf import get_token
from django.urls import path

from .employeeViews import employee_views, employee_list_json, get_employee_info, create_employee_from_api
from .roleViews import group_list, create_group, create_default_groups, set_now_role, get_user_groups
from .studentViews import save_student_from_api, create_student_from_api, get_student_info
from .views import login_view, logout, student_list, employee_list, user_list

login_patterns = [
    path('login', login_view, name='login'),
    path('logout', logout, name='logout'),
]


student_patterns = [
    path('save_student_from_api', save_student_from_api, name='save_student_from_api'),
    path('create_student_from_api', create_student_from_api, name='create_student_from_api'),
    path('get_student_info', get_student_info, name='get_student_info'),
]
employee_patterns = [
    path('employee_list/', employee_views, name='employeeViews'),
    path('employee_list_json', employee_list_json, name='employee_list_json'),
    path('get_employee_info', get_employee_info, name='get_employee_info'),
    path('create_employee_from_api', create_employee_from_api, name='create_employee_from_api'),
]

role_permissions = [
    path('group_list_api', group_list, name='group_list'),
    path('create_group_api', create_group, name='create_group'),
    path('create_default_groups', create_default_groups, name='create_default_groups'),
    path('get_user_groups', get_user_groups, name='get_user_groups'),
    path('set_now_role', set_now_role, name='set_now_role'),

]



views_patterns = [
    # Hodimlar haqida ma'lumotni olish uchun URL
    path('student_list', student_list, name='student_list'),
    path('employee_list', employee_list, name='employee_list'),
    path('user_list', user_list, name='user_list'),

]

urlpatterns = views_patterns + login_patterns + role_permissions
