# Generated by Django 3.0.10 on 2020-11-12 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0096_auto_20201030_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='capacity',
            field=models.PositiveIntegerField(blank=True, default=100, help_text='The max number of event registrants', null=True),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='close_registration',
            field=models.BooleanField(default=False, help_text="To close an event's registration"),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='time_zone',
            field=models.CharField(choices=[('US/Eastern', 'Eastern'), ('US/Central', 'Central'), ('US/Mountain', 'Mountain'), ('US/Pacific', 'Pacific')], default='US/Central', max_length=16, verbose_name='Time Zone'),
        ),
    ]
