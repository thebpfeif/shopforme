# Generated by Django 2.1 on 2018-08-05 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_manager', '0002_auto_20180805_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='weight_units',
            field=models.CharField(default='None', max_length=10),
        ),
        migrations.AlterField(
            model_name='item',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='weight',
            field=models.FloatField(default=0),
        ),
    ]
