# Generated by Django 4.1.2 on 2022-10-20 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='name',
            field=models.CharField(default=1, max_length=2056),
            preserve_default=False,
        ),
    ]