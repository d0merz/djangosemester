# Generated by Django 3.0.5 on 2020-05-09 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200509_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский')], default='M', max_length=1),
        ),
    ]
