# Generated by Django 5.1.5 on 2025-02-13 15:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notentabelle', '0007_semester_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester_marks',
            name='semester_1',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15)]),
        ),
        migrations.AlterField(
            model_name='semester_marks',
            name='semester_2',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15)]),
        ),
        migrations.AlterField(
            model_name='semester_marks',
            name='semester_3',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15)]),
        ),
        migrations.AlterField(
            model_name='semester_marks',
            name='semester_4',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15)]),
        ),
    ]
