# Generated by Django 3.1.7 on 2021-05-27 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit_type',
            field=models.CharField(choices=[('KILOGRAM', 'Kilogram'), ('LITER', 'Liter'), ('DOZEN', 'Dozen'), ('PIECE', 'Piece'), ('CUSTOM', 'Custom')], max_length=20),
        ),
    ]
