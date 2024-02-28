# Generated by Django 4.2 on 2024-02-27 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_posicion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Afectacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('codigo', models.CharField(max_length=50)),
                ('activo', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Afectacion',
                'verbose_name_plural': 'Afectaciones',
            },
        ),
    ]
