# Generated by Django 5.1.2 on 2024-11-13 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSElist4', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='Default Category', max_length=100),
        ),
    ]
