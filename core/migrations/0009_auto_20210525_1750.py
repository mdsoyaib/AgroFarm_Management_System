# Generated by Django 3.1.7 on 2021-05-25 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210525_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
