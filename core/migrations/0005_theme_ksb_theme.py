# Generated by Django 5.2.1 on 2025-05-28 15:57

import django.db.models.deletion
import uuid
from django.db import migrations, models

def seed_themes(apps, schema_editor):
    Theme = apps.get_model('core', 'Theme')
    Theme.objects.bulk_create([
        Theme(id= 1,name='Code Quality'),
        Theme(id= 2,name='Meeting User Needs'),
        Theme(id= 3,name='The CI-CD Pipeline'),
        Theme(id= 4,name='Refreshing and Patching'),
        Theme(id= 5,name='Operability'),
        Theme(id= 6,name='Data Persistence'),
        Theme(id= 7,name='Automation'),
        Theme(id= 8,name='Data Security'),
    ])
class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_seed_ksbs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='ksb',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.theme'),
            preserve_default=False,
        ),
        migrations.RunPython(seed_themes),
    ]
