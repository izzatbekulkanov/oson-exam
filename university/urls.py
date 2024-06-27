from django.urls import path

from .json.views import get_universities_token_data, get_universities_data, update_api_token_view, \
    save_departments_from_api, save_specialty_from_api, save_curriculum_from_api, save_group_from_api, \
    update_university_status, save_university_from_api
from .views import (
    university_dashboard, university_data, api_token_view, )

other_urlpatterns = [
    path('', university_dashboard, name='university_dashboard'),
]

update_ulrpatterns = [
    path('save_university_from_api', save_university_from_api, name='save_university_from_api'),
    path('save_departments_from_api', save_departments_from_api, name='save_departments_from_api'),
    path('save_specialty_from_api', save_specialty_from_api, name='save_specialty_from_api'),
    path('save_curriculum_from_api', save_curriculum_from_api, name='save_curriculum_from_api'),
    path('save_group_from_api', save_group_from_api, name='save_group_from_api'),
]
json_urlpatterns = [
    path('get_universities_token_data', get_universities_token_data, name='get_universities_token_data'),
    path('get_universities_data', get_universities_data, name='get_universities_data'),
    path('update_university_status', update_university_status, name='update_university_status'),
    path('update_api_token_view', update_api_token_view, name='update_api_token_view'),


]
views_urlpatterns = [
    path('api_token_view', api_token_view, name='api_token_view'),
    path('university_data', university_data, name='university_data'),
]


urlpatterns = other_urlpatterns +  views_urlpatterns + json_urlpatterns + update_ulrpatterns