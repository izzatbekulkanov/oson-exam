from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from university.models import Level
from .models import CustomUser, StudentType, StudentStatus, Citizenship, District, Province, Country, EmployeeType, \
    EmployeeStatus, Gender, StaffPosition, PaymentForm, Accommodation, Roles


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'full_name', 'is_active', 'full_id', 'now_role', 'user_type']
    list_filter = ['is_active']
    search_fields = ['username', 'email', 'full_name', 'first_name', 'last_name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'password_save', 'full_id', 'user_type', 'department')}),
        ('Personal info', {'fields': ('first_name', 'second_name', 'third_name', 'gender',  'full_name', 'image', 'imageFile','phone_number', 'birth_date', 'university')}),
        ('Student info', {'fields': ('student_id_number', 'group', 'level', 'semester', 'educationYear', 'year_of_enter', 'studentType', 'paymentForm', 'studentStatus')}),
        ('Employee info', {'fields': ('employee_id_number', 'employeeStatus', 'contractDate', 'staffPosition', 'employeeType', 'is_employee')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_followers_book', 'now_role', 'groups', 'user_permissions', 'hemis_role')}),
        ('secret', {'fields': ('hash', 'token', 'telegram', 'instagram', 'facebook')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'full_name', 'image', 'phone_number',
                       'birth_date', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
         ),
    )

    ordering = ['-created_at']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Permission)

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(Roles)
class PaymentFormAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(PaymentForm)
class PaymentFormAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(EmployeeStatus)
class EmployeeStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(EmployeeType)
class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(StaffPosition)
class StaffPosition(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(Citizenship)
class CitizenshipAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(StudentType)
class StudentTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(StudentStatus)
class StudentStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

