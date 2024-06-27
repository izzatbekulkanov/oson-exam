from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import BookListAPIView, LibraryListAPIView

# Swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title="Namangan Davlat Pedagogika Instituti Kutubxona Boshqaruv API",
        default_version='v1',
        description=(
            "Ushbu API kutubxona tizimini boshqarish uchun foydalanuvchilarga imkon beradi, jumladan, kitoblar, mualliflar, "
            "kitob turlari, BBK tasniflari, kutubxonalar va kitob nusxalari haqida ma'lumotlarni boshqarish. Foydalanuvchilar "
            "ushbu resurslar ustida CRUD amallarini bajarishlari va turli mezonlar bo'yicha kitoblarni qidirishlari va "
            "filtrlashlari mumkin.\n\n"
            "**Dasturchi**: Izzatbek Ulkanov\n"
            "**Institut**: Namangan Davlat Pedagogika Instituti"
        ),
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="izzatbek@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(),  # Agar sizga autentifikatsiya kerak bo'lsa, bu qatorni olib tashlang
)

# Swagger UI URLs
urlpatterns = [
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('libraries/', LibraryListAPIView.as_view(), name='library-list'),
    path('api-auth/', include('rest_framework.urls')),  # Include DRF auth URLs
]