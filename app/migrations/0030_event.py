# Generated by Django 3.0.4 on 2020-03-18 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_merge_20191205_2106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(help_text='Name of the event', max_length=255)),
                ('event_type', models.CharField(choices=[('benefits_meeting', 'Benefits Meeting'), ('benefits_training', 'Benefits Training'), ('webcast', 'Compliance Webcast'), ('tradeshow', 'Tradeshow')], default='', max_length=24)),
                ('location_type', models.CharField(choices=[('online', 'Online'), ('in_person', 'In Person')], default='', max_length=24)),
                ('address_line_1', models.CharField(default='', max_length=255)),
                ('address_line_2', models.CharField(default='', max_length=255)),
                ('address_city', models.CharField(default='', max_length=255)),
                ('address_state', models.CharField(default='', max_length=255)),
                ('address_zipcode', models.CharField(default='', max_length=255)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('cost', models.CharField(default='Free', max_length=50)),
            ],
            options={
                'ordering': ['event_title'],
            },
        ),
    ]
