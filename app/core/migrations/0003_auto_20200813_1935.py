# Generated by Django 3.0.5 on 2020-08-13 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200810_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='bmi',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='patient',
            name='height',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone',
            field=models.CharField(default='0', max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='sex',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=6),
        ),
    ]
