# Generated by Django 2.1.2 on 2019-04-20 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_auto_20190420_1329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuenta',
            name='id_cuenta',
        ),
        migrations.AlterField(
            model_name='cuenta',
            name='rut',
            field=models.CharField(max_length=15, primary_key=True, serialize=False),
        ),
    ]
