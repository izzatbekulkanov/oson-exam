from rest_framework import serializers
from .models import University, Specialty, Curriculum, Department, GroupUniver
from rest_framework.response import Response


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['name', 'code', 'api_url', 'api_token', 'student_url', 'employee_url', 'is_active']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'codeID', 'parent', 'active', 'structure_type']

class SpecialtySerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    education_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Specialty
        fields = ['name', 'codeID', 'department_name', 'education_type_name']

    def get_department_name(self, obj):
        return obj.department.name

    def get_education_type_name(self, obj):
        return obj.educationType.name

class CurriculumSerializer(serializers.ModelSerializer):
    specialty_name = serializers.SerializerMethodField()
    education_type_name = serializers.SerializerMethodField()
    education_form_name = serializers.SerializerMethodField()

    class Meta:
        model = Curriculum
        fields = ['name', 'codeID', 'specialty_name', 'education_type_name', 'education_form_name', 'education_period']

    def get_specialty_name(self, obj):
        return obj.specialty.name

    def get_education_type_name(self, obj):
        return obj.educationType.name

    def get_education_form_name(self, obj):
        return obj.educationForm.name

class GroupUniverSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')
    specialty_name = serializers.ReadOnlyField(source='specialty.name')
    curriculum_name = serializers.ReadOnlyField(source='curriculum.name')

    class Meta:
        model = GroupUniver
        fields = ['name', 'codeID', 'department_name', 'specialty_name', 'curriculum_name']


