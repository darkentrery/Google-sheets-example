# Generated by Django 4.2 on 2023-04-04 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplies', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supply',
            options={'ordering': ['number'], 'verbose_name': 'Supply', 'verbose_name_plural': 'Supplies'},
        ),
        migrations.AddField(
            model_name='supply',
            name='is_send',
            field=models.BooleanField(default=False, verbose_name='Expired message is send'),
        ),
    ]
