# Generated by Django 5.0.4 on 2024-05-07 16:34

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_contract_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='file',
            field=models.FileField(blank=True, default=None, storage=django.core.files.storage.FileSystemStorage(location='/home/alex/data/personal/kollektiivi/website/accounts/'), upload_to=''),
        ),
    ]