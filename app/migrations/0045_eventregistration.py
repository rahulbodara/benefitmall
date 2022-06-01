# Generated by Django 3.0.4 on 2020-03-24 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_auto_20200323_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=255, verbose_name='First Name')),
                ('last_name', models.CharField(default='', max_length=255, verbose_name='Last Name')),
                ('company', models.CharField(default='', max_length=255, verbose_name='Company')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(default='', max_length=16, verbose_name='Phone')),
                ('address1', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Address Line 1')),
                ('address2', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Address Line 2')),
                ('city', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='State')),
                ('postalcode', models.CharField(default='', max_length=16, verbose_name='Postal Code')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='registered_event', to='app.Event')),
            ],
        ),
    ]
