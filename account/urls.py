from django.middleware.csrf import get_token
from django.urls import path

from .employeeViews import employee_views, employee_list_json, get_employee_info, \
    create_employee_from_api
from .json.get_employee import get_employee_users, get_employee_details, save_employee_groups
from .json.get_student import get_student_users
from .json.password_change import change_password
from .json.profile import get_user_all_groups, get_user_roles, get_employee_user_information, get_user_book_loans
from .json.updateStudent.create_employee import create_employee
from .json.update_profile import update_passport_serial, update_passport_jshshir, update_social_media, \
    update_employee_profile_from_api, update_student_profile_from_api
from .roleViews import group_list, create_group, create_default_groups, set_now_role, get_user_groups
from .studentViews import save_student_from_api, create_student_from_api, get_student_info
from .views import (login_view, create_student, student_list, permission_view, logout_view,
                    create_employee_view, hemis_view, profile_view, employee_view, student_view)

login_patterns = [
    path('login', login_view, name='login'),
    path('logout_view', logout_view, name='logout'),

]

update_employee_patterns = [
    path('change_password', change_password, name='change_password'),
    path('update_passport_serial', update_passport_serial, name='update_passport_serial'),
    path('update_passport_jshshir', update_passport_jshshir, name='update_passport_jshshir'),
    path('update_social_media', update_social_media, name='update_social_media'),

    path('get_user_all_groups', get_user_all_groups, name='get_user_all_groups'),
    path('get_user_roles', get_user_roles, name='get_user_roles'),
    path('get_employee_user_information', get_employee_user_information, name='get_employee_user_information'),
    path('get_user_book_loans', get_user_book_loans, name='get_user_book_loans'),
    path('update_employee_profile_from_api', update_employee_profile_from_api, name='update_employee_profile_from_api'),
    path('update_student_profile_from_api', update_student_profile_from_api, name='update_student_profile_from_api'),

]

student_patterns = [
    path('save_student_from_api', save_student_from_api, name='save_student_from_api'),
    path('create_student_from_api', create_student_from_api, name='create_student_from_api'),
    path('get_student_info', get_student_info, name='get_student_info'),
    path('create_student', create_student, name='create_student'),
    path('student_list', student_list, name='student_list'),
]
employee_patterns = [
    path('employee_list/', employee_views, name='employeeViews'),
    path('employee_list_json', employee_list_json, name='employee_list_json'),
    path('create_employee', create_employee_view, name='create_employee'),
    path('get_employee_info', get_employee_info, name='get_employee_info'),
    path('create_employee_from_api', create_employee_from_api, name='create_employee_from_api'),
]

role_permissions = [
    path('permissions', permission_view, name='permission_view'),
    path('group_list_api', group_list, name='group_list'),
    path('create_group_api', create_group, name='create_group'),
    path('create_default_groups', create_default_groups, name='create_default_groups'),
    path('get_user_groups', get_user_groups, name='get_user_groups'),
    path('set_now_role', set_now_role, name='set_now_role'),

]

hemis_patterns = [
    path('hemis_view', hemis_view, name='hemis_view'),
    path('profile_view', profile_view, name='profile_view'),

]

json_patterns = [
    path('get_employee_users', get_employee_users, name='get_employee_users'),
    path('get_student_users', get_student_users, name='get_student_users'),
    path('create_employee', create_employee, name='create_employee'),
    path('save_employee_groups', save_employee_groups, name='save_employee_groups'),

]

views_patterns = [
    path('employee_view', employee_view, name='employee_view'),
    path('student_view', student_view, name='student_view'),
    # Hodimlar haqida ma'lumotni olish uchun URL
    path('employees/<int:id>/', get_employee_details, name='get_employee_details'),
]

urlpatterns = views_patterns + json_patterns + login_patterns + update_employee_patterns + role_permissions
