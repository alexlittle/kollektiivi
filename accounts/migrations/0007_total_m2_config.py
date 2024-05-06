from django.db import migrations


def add_initial_config(apps, schema_editor):
    Config = apps.get_model("accounts", "Config")
    c1, _ = Config.objects.get_or_create(name="total_rentable_m2")
    c1.value = "190"
    c1.save()



class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0006_contract_contact_name'),
    ]

    operations = [
        migrations.RunPython(add_initial_config),
    ]
