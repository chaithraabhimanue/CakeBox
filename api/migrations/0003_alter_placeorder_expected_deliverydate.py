# Generated by Django 4.1.3 on 2023-05-02 05:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_addtocart_cake_placeorder_reviews_delete_cakebox_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeorder',
            name='expected_deliverydate',
            field=models.DateTimeField(default=datetime.date(2023, 5, 3)),
        ),
    ]