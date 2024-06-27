# Generated by Django 5.0.6 on 2024-05-20 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_alter_book_bbk'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcopy',
            name='status',
            field=models.CharField(choices=[('accepted', 'Qabul qilindi'), ('not_accepted', 'Qabul qilinmagan')], default='rejected', help_text='Kitob holati', max_length=20),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('distributed', 'Yakunlangan'), ('undistributed', 'Yakunlanmagan')], default='rejected', help_text='Kitob holati', max_length=20),
        ),
    ]
