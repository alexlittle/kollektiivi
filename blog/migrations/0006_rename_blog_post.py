# Generated by Django 4.2.1 on 2023-06-25 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blog_body_alter_blog_body_en_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blog',
            new_name='Post',
        ),
    ]
