# Generated by Django 5.1.5 on 2025-01-21 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0002_alter_uploadalert_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadalert',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
