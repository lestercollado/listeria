# Generated by Django 4.2 on 2024-02-27 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_persona_disponible_persona_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='cargo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.cargo'),
            preserve_default=False,
        ),
    ]
