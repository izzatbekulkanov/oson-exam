# Generated by Django 5.0.6 on 2024-05-25 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_alter_bookcopy_send_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcopy',
            name='send_date',
            field=models.DateTimeField(blank=True, help_text='Last send time of the book', null=True),
        ),
    ]