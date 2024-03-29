# Generated by Django 3.2.3 on 2021-07-04 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=500)),
                ('category', models.CharField(default='none', max_length=100)),
                ('cutPrice', models.IntegerField()),
                ('price', models.FloatField()),
                ('image', models.ImageField(upload_to='static/app/images/product')),
            ],
        ),
    ]
