# Generated by Django 4.2.1 on 2023-06-22 17:59

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='body_en',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='body_fi',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='title_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='title_fi',
            field=models.TextField(null=True),
        ),
    ]