# Generated by Django 3.0.4 on 2020-03-26 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0059_auto_20200326_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='background_color',
            field=models.CharField(choices=[('bg--light', 'Light'), ('bg--primary', 'Primary'), ('bg--secondary', 'Secondary'), ('bg--dark', 'Dark')], default='bg--light', max_length=50),
        ),
        migrations.AddField(
            model_name='notification',
            name='text_alignment',
            field=models.CharField(choices=[('', 'Align Left'), ('text-center', 'Align Center'), ('text-right', 'Align Right')], default='', max_length=50),
        ),
    ]
