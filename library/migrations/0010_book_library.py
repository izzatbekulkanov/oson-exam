# Generated by Django 5.0.6 on 2024-05-21 05:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_alter_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='library',
            field=models.ForeignKey(blank=True, help_text='Kitob kutubxonasi', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='library.library'),
        ),
    ]
