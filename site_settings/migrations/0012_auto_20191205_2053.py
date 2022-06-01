# Generated by Django 2.2.7 on 2019-12-05 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0011_auto_20190705_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='apple_touch_icon',
            field=models.ForeignKey(blank=True, help_text='The apple touch icon should be 114 x 114 or 144 x 144, and a png file.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='touch_icon', to='wagtailimages.Image', verbose_name='Apple Touch Icon'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='favicon_ico',
            field=models.ForeignKey(blank=True, help_text='The favicon must be 16x16 pixels or 32x32 pixels, using either 8-bit or 24-bit colors. The format of the image must be one of PNG (a W3C standard), GIF, or ICO.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favicon', to='wagtailimages.Image', verbose_name='Favicon'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='pwa_icon_large',
            field=models.ForeignKey(blank=True, help_text='This icon should be a 512x512 pixel png file', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='large_icon', to='wagtailimages.Image', verbose_name='Large Icon'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='pwa_icon_small',
            field=models.ForeignKey(blank=True, help_text='This icon should be a 192x192 pixel png file', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='small_icon', to='wagtailimages.Image', verbose_name='Small Icon'),
        ),
    ]
