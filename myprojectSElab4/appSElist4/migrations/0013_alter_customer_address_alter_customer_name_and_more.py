# Generated by Django 5.1.2 on 2024-12-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSElist4', '0012_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
