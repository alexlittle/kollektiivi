# Generated by Django 5.0.4 on 2024-05-03 07:40

import django.utils.timezone
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Config',
                'verbose_name_plural': 'Config',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contact_info', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('business_id', models.CharField(blank=True, default=None, max_length=20)),
                ('active', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('meters_sq', models.DecimalField(decimal_places=1, default=0, max_digits=10)),
                ('deposit_held', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('on_statement', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=100)),
                ('sales_tax_charged', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('sales_tax_paid', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('sales_tax_rate', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('file', models.FileField(blank=True, default=None, upload_to='transaction')),
            ],
        ),
    ]