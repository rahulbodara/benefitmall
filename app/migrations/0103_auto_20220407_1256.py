# Generated by Django 3.0.14 on 2022-04-07 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0010_document_file_hash'),
        ('wagtailimages', '0022_uploadedimage'),
        ('app', '0102_auto_20220406_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinarpage',
            name='document',
            field=models.ForeignKey(help_text='Please select Internal Document', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document', verbose_name='Document'),
        ),
        migrations.AddField(
            model_name='webinarpage',
            name='type',
            field=models.CharField(choices=[('internal', 'Internal'), ('external', 'External')], default='internal', max_length=8),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='image',
            field=models.ForeignKey(help_text='Image Dimensions 200x230px', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Image'),
        ),
    ]
