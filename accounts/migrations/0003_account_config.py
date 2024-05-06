from django.db import migrations


def add_initial_config(apps, schema_editor):
    Config = apps.get_model("accounts", "Config")
    c1, _ = Config.objects.get_or_create(name="org_name")
    c1.value = "Kollektiivi Joensuu ry"
    c1.save()

    c1, _ = Config.objects.get_or_create(name="org_address")
    c1.value = "Sortavalankatu 2, 80100 Joensuu"
    c1.save()

    c2, _ = Config.objects.get_or_create(name="account_iban")
    c2.value = ""
    c2.save()

    c2, _ = Config.objects.get_or_create(name="account_bic")
    c2.value = ""
    c2.save()

    c2, _ = Config.objects.get_or_create(name="y_tunnus")
    c2.value = "FI 3433889-4"
    c2.save()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_initial_config'),
    ]

    operations = [
        migrations.RunPython(add_initial_config),
    ]
