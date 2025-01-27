# Generated by Django 5.1.5 on 2025-01-27 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stundenplan', '0017_lesson_room_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='teachers',
        ),
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.IntegerField(unique=True),
        ),
        migrations.DeleteModel(
            name='Teacher_Class',
        ),
    ]
