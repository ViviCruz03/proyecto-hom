# Generated by Django 5.1.7 on 2025-03-25 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_rename_status_unieconomicas_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unieconomicas',
            name='estado',
            field=models.CharField(choices=[('Prospecto', 'Prospecto'), ('Cliente Nuevo', 'Cliente Nuevo'), ('Ya era Cliente', 'Ya era Cliente'), ('Descartado', 'Descartado')], default='Prospecto', max_length=50),
        ),
    ]
