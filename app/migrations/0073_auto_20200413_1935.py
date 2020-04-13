# Generated by Django 3.0.5 on 2020-04-13 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0072_auto_20200409_2048'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('old_guid', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('show_on_division_page', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address_1', models.CharField(blank=True, max_length=50, null=True)),
                ('address_2', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('tollfree_number', models.CharField(blank=True, max_length=50, null=True)),
                ('fax_number', models.CharField(blank=True, max_length=50, null=True)),
                ('latlng', models.CharField(blank=True, max_length=255, null=True)),
                ('old_guid', models.CharField(blank=True, max_length=40, null=True)),
                ('business_type', models.ManyToManyField(related_name='location_business_types', to='app.BusinessType')),
                ('division', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='location_state', to='app.Division')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('abbreviation', models.CharField(max_length=2)),
                ('old_guid', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('show_email', models.BooleanField(default=False)),
                ('is_executive', models.BooleanField(default=False)),
                ('executive_order', models.IntegerField()),
                ('bio', models.TextField()),
                ('is_archived', models.BooleanField(default=False)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_location', to='app.Location')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='location_state', to='app.State'),
        ),
        migrations.AddField(
            model_name='division',
            name='states',
            field=models.ManyToManyField(related_name='division_states', to='app.State'),
        ),
        migrations.AddField(
            model_name='division',
            name='vice_president',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='division_vp', to='app.Person'),
        ),
    ]
