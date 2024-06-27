import json

from django.contrib import admin
from django.utils.html import format_html

from .models import University, Department, Specialty, GroupUniver, EducationLang, Semester, Level, EducationForm, \
    EducationType, Curriculum, SubjectDetail, TrainingType, Subject, EducationYear


# University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'api_url', 'student_url', 'employee_url', 'api_token_display')

    def api_token_display(self, obj):
        if obj.api_token is not None:
            try:
                token_dict = json.loads(obj.api_token)
                token_html = '<pre>{}</pre>'.format(json.dumps(token_dict, indent=4))
                return format_html(token_html)
            except json.JSONDecodeError:
                return obj.api_token
        else:
            return None

    api_token_display.short_description = 'API Token JSON'
# Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'active')

# Specialty
@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code' ,'codeID')

# Group
@admin.register(GroupUniver)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'codeID' , 'educationLang')

# EducationLang
@admin.register(EducationLang)
class EducationLangAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

# Semester
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

# Level
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

# EducationForm
@admin.register(EducationForm)
class EducationFormAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

# EducationType
@admin.register(EducationType)
class EducationTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

# Curriculum
@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('specialty', 'educationType', 'educationForm', 'name', 'semester_count', 'education_period', 'codeID')

# SubjectDetail
@admin.register(SubjectDetail)
class SubjectDetailAdmin(admin.ModelAdmin):
    list_display = ('trainingType', 'academic_load')


@admin.register(EducationYear)
class EducationYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

# TrainingType
@admin.register(TrainingType)
class TrainingTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

# Subject
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject', 'semester', 'department', 'total_acload', 'credit', 'resource_count', 'in_group', 'at_semester', 'created_at', 'updated_at')
    filter_horizontal = ('subjectDetails',)
