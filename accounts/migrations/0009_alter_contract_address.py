# Generated by Django 5.0.4 on 2024-05-06 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_contact_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='address',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
