from rest_framework import serializers
from .models import University, Specialty, Curriculum, Department, GroupUniver
from rest_framework.response import Response


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['name', 'code', 'api_url', 'api_token', 'student_url', 'employee_url']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'codeID', 'parent', 'active', 'structure_type']

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['name', 'codeID', 'department', 'educationType']

class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = ['name', 'codeID', 'specialty', 'educationType', 'educationForm', 'education_period']

class GroupUniverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = ['name', 'codeID']

