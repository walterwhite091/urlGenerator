# Generated by Django 3.2.12 on 2022-02-15 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlGenerator', '0011_alter_link_hit_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='shorten_url',
            field=models.URLField(blank=True, default=''),
        ),
    ]
