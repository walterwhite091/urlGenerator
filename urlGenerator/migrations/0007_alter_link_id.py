# Generated by Django 3.2.12 on 2022-02-04 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlGenerator', '0006_alter_link_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
