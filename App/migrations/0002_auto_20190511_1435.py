# Generated by Django 2.1.2 on 2019-05-11 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='id_evento',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='id_reserva',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
