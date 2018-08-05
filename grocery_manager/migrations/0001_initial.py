# Generated by Django 2.1 on 2018-08-05 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('name', models.CharField(max_length=250)),
                ('brand', models.CharField(max_length=100)),
                ('count', models.IntegerField()),
                ('weight', models.IntegerField()),
            ],
        ),
    ]