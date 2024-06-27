# Generated by Django 5.0.6 on 2024-05-30 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_book_authorcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcopy',
            name='haveStatus',
            field=models.CharField(choices=[('yes', 'Mavjud'), ('no', 'Mavjud eas')], default='yes', help_text='Kitob berilganlik holati', max_length=20),
        ),
    ]