# Generated by Django 4.2.1 on 2023-06-23 12:12

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kollektiivi', '0003_member'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['order_by', 'name'], 'verbose_name': 'Jäsen', 'verbose_name_plural': 'Jäseniä'},
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['menu_order_by', 'title'], 'verbose_name': 'Page', 'verbose_name_plural': 'Pages'},
        ),
        migrations.AddField(
            model_name='member',
            name='contact',
            field=ckeditor.fields.RichTextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='contact_en',
            field=ckeditor.fields.RichTextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='contact_fi',
            field=ckeditor.fields.RichTextField(blank=True, default=None, null=True),
        ),
    ]
