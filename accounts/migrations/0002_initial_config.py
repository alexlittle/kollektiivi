from django.db import migrations


def add_initial_config(apps, schema_editor):
    Config = apps.get_model("accounts", "Config")
    c1, _ = Config.objects.get_or_create(name="vr_deposit")
    c1.value = "3274.0"
    c1.save()

    c1, _ = Config.objects.get_or_create(name="alv_rate")
    c1.value = "24"
    c1.save()

    c2, _ = Config.objects.get_or_create(name="m2_rate_ex_alv")
    c2.value = "1"
    c2.save()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_config),
    ]
