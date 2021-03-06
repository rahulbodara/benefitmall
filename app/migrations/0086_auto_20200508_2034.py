# Generated by Django 3.0.5 on 2020-05-08 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0085_auto_20200508_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headerfooter',
            name='featured_event_bg_invert',
            field=models.CharField(choices=[('', 'Dark'), ('image--light', 'Light')], default='', help_text='Invert the image overlay', max_length=50, verbose_name='Invert Dark/Light'),
        ),
        migrations.AlterField(
            model_name='headerfooter',
            name='featured_news_bg_invert',
            field=models.CharField(choices=[('', 'Dark'), ('image--light', 'Light')], default='', help_text='Invert the image overlay', max_length=50, verbose_name='Invert Dark/Light'),
        ),
    ]
