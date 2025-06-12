from django.db import migrations

def seed_themes_into_ksbs(apps, schema_editor):
    Theme = apps.get_model('core', 'Theme')
    KSB = apps.get_model('core', 'KSB')

    theme_map = {
        1: ['K2', 'K5', 'K7', 'K14', 'S9', 'S11', 'S14', 'S17', 'S18', 'S20', 'S22'],
        2: ['K4', 'K10', 'K21', 'S3'],
        3: ['K1', 'K15', 'S15'],
        4: ['K8', 'S5'],
        5: ['K11', 'S6', 'S19', 'B3'],
        6: ['K12', 'S7'],
        7: ['K13', 'K17', 'S12'],
        8: ['K16', 'S10'],
    }

    for theme_id, ksb_codes in theme_map.items():
        theme = Theme.objects.get(id=theme_id)
        for ksb_code in ksb_codes:
            try:
                ksb = KSB.objects.get(name=ksb_code)
                ksb.theme = theme
                ksb.save()
            except KSB.DoesNotExist:
                print(f"KSB with code {ksb_code} not found.")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_theme_ksb_theme'),
    ]

    operations = [
        migrations.RunPython(seed_themes_into_ksbs),
    ]
