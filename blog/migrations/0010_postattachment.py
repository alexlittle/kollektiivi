# Generated by Django 4.2.7 on 2023-11-24 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_post_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='post_files')),
                ('title', models.TextField()),
                ('order_by', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Post Attachment',
                'verbose_name_plural': 'Post Attachments',
            },
        ),
    ]
