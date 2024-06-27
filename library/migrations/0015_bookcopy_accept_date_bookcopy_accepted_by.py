# Generated by Django 5.0.6 on 2024-05-25 10:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_alter_bookcopy_send_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcopy',
            name='accept_date',
            field=models.DateTimeField(blank=True, help_text='Last accept time of the book', null=True),
        ),
        migrations.AddField(
            model_name='bookcopy',
            name='accepted_by',
            field=models.ForeignKey(default=1, help_text='Kitobni qabul qilgan foydalanuvchi', on_delete=django.db.models.deletion.CASCADE, related_name='accepted_books', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]