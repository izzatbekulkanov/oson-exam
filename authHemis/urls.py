from django.urls import path

from .viewsStudent import OAuthAuthorizationStudentView, OAuthCallbackStudentView
from .viewsEmployee import OAuthAuthorizationView, OAuthCallbackView

urlpatterns = [
    path('authorize/', OAuthAuthorizationView.as_view(), name='oauth_authorize'),
    path('authorize/student/', OAuthAuthorizationStudentView.as_view(), name='student_oauth_authorize'),
    path('callback', OAuthCallbackView.as_view(), name='oauth_callback'),
    path('callback/student', OAuthCallbackStudentView.as_view(), name='oauth_callback'),

]
