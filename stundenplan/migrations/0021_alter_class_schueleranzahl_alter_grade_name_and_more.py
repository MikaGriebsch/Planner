# Generated by Django 5.1.5 on 2025-01-27 20:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stundenplan', '0020_alter_class_name_alter_subject_abkuerzung_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='schueleranzahl',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(40)]),
        ),
        migrations.AlterField(
            model_name='grade',
            name='name',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(13)]),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_number',
            field=models.CharField(max_length=3, unique=True),
        ),
        migrations.AlterField(
            model_name='subject_grade',
            name='wochenstunden',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
