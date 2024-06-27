# Generated by Django 5.0.6 on 2024-05-20 09:38

import library.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_remove_book_library_bookcopy_library_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default=library.models.get_default_book_cover, help_text="Kitob rasmi (mavjud bo'lsa)", null=True, upload_to='book_covers/'),
        ),
    ]
