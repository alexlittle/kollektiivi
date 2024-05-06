from django.db import migrations


def add_initial_config(apps, schema_editor):
    Config = apps.get_model("accounts", "Config")
    c1, _ = Config.objects.get_or_create(name="account_bank")
    c1.value = "OP"
    c1.save()

    c1, _ = Config.objects.get_or_create(name="contact_name")
    c1.value = "Alex"
    c1.save()

    c1, _ = Config.objects.get_or_create(name="contact_phone")
    c1.value = "0456402013"
    c1.save()

    c1, _ = Config.objects.get_or_create(name="contact_email")
    c1.value = "info@kollektiivi.org"
    c1.save()



class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0007_total_m2_config'),
    ]

    operations = [
        migrations.RunPython(add_initial_config),
    ]
