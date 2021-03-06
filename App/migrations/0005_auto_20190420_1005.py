# Generated by Django 2.1.2 on 2019-04-20 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuenta',
            name='correoAsociado',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='esactiva',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='fecha_registro',
            field=models.DateField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='tipo_usuario',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
