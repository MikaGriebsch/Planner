# Generated by Django 5.1.5 on 2025-01-20 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stundenplan', '0002_lehrer_class'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Lehrer',
            new_name='Teacher',
        ),
        migrations.CreateModel(
            name='Teached_Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('klasse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stundenplan.class')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stundenplan.teacher')),
            ],
        ),
        migrations.AlterField(
            model_name='class',
            name='teachers',
            field=models.ManyToManyField(through='stundenplan.Teached_Subjects', to='stundenplan.lehrer'),
        ),
    ]
