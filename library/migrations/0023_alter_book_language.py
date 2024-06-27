# Generated by Django 5.0.6 on 2024-06-11 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0022_book_bookcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(choices=[('en', 'Ingliz'), ('tr', 'Turk'), ('fr', 'Fransuz'), ('uz', "O'zbek (lotin)"), ('oz', "O'zbek (kril)"), ('ru', 'Rus'), ('de', 'Nemis'), ('zh', 'Xitoy'), ('es', 'Ispan'), ('ko', 'Koreys'), ('kk', 'Qozoq'), ('ky', "Qirg'iz"), ('tg', 'Tojik'), ('qr', 'Qoraqalpoq')], help_text='Kitob tili', max_length=100),
        ),
    ]
