# Generated by Django 5.1.5 on 2025-01-20 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stundenplan', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
            ],
        ),
    ]
