from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ...models import CustomUser
from ...serializers import CustomUserSerializer
from django.contrib.auth.models import Group

class LibraryAndAdminUsersView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # Agar autentifikatsiya talab qilinmasa, bu qatorni olib tashlang

    def get_queryset(self):
        # Library va LibraryAdmin Group ga a'zo bo'lgan foydalanuvchilarni olish
        library_group = Group.objects.get(name='Library')
        library_admin_group = Group.objects.get(name='LibraryAdmin')
        return CustomUser.objects.filter(groups__in=[library_group, library_admin_group]).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
