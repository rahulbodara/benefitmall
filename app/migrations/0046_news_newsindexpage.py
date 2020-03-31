# Generated by Django 3.0.4 on 2020-03-24 23:02

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.routable_page.models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_eventregistration'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_slug', models.SlugField(blank=True, max_length=255, null=True, verbose_name='URL Name')),
                ('news_title', models.CharField(max_length=255, verbose_name='Title')),
                ('news_datetime', models.DateTimeField(help_text='The date and time of the press release.', verbose_name='Date & Time')),
                ('body', wagtail.core.fields.RichTextField(default='', verbose_name='Body')),
            ],
            options={
                'ordering': ['news_datetime'],
            },
        ),
        migrations.CreateModel(
            name='NewsIndexPage',
            fields=[
                ('defaultpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.DefaultPage')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'app.defaultpage'),
        ),
    ]
