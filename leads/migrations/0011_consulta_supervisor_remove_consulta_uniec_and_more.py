# Generated by Django 5.1.7 on 2025-03-26 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0010_alter_unieconomicas_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='supervisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.supervisor', verbose_name='Supervisor'),
        ),
        migrations.RemoveField(
            model_name='consulta',
            name='uniEc',
        ),
        migrations.AddField(
            model_name='consulta',
            name='uniEc',
            field=models.ManyToManyField(to='leads.unieconomicas', verbose_name='Unidades Economicas'),
        ),
    ]
